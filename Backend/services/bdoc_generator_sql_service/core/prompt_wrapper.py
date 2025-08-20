"""
This module provides a wrapper class for executing prompts based on a tag and request data.
It handles the execution of SQL prompts,
manages user counts, and updates the database with the results.
It is designed to be used in an asynchronous environment,
allowing for efficient execution of multiple prompts without blocking the event loop.
It also includes methods for checking user
or IP address counts and updating the database after prompt execution.
"""
import hashlib
import re
import os
from logging import Logger
from typing import Optional
from fastapi import Request
from fastapi.responses import JSONResponse
from core.jwt_lib import JWTLibrary
from core.db_service import DBService
from core.database_connection import AsyncSQLAlchemySingleton
from core.custom_logger import CustomLogger
from core.prompt import Prompt
from models.requests import Requests

class PromptWrapper:
    """
    Wrapper class for executing prompts based on a tag and request data.
    """
    def __init__(
            self,
            tag: str,
            request: Request,
            request_json: dict,
            jwt_token: Optional[str],
            db_connection: AsyncSQLAlchemySingleton,
            logger: Logger = CustomLogger.setup_logger(__name__)
        ):
        """
        Initializes the PromptWrapper with the provided parameters.
        Args:
            tag (str): The tag associated with the prompt.
            request (dict): The request data.
            jwt_token (Optional[str]): The JWT token string.
            logger (custom_logger): The logger instance for logging.
        """
        # Initialize instance variables
        self.tag = tag
        self.request = request
        self.request_json = request_json
        self.jwt_token = jwt_token
        self.db_connection = db_connection
        self.logger = logger

        # Derive SQL Script and Business Name from request
        self.sql_script = self.request_json.get("script", None)
        self.business_name = self.request_json.get("business", None)

        # Initialize JWT Library
        self.jwt_lib = JWTLibrary(logger=self.logger)

        # Initialize Count Service
        self.db_service = DBService(
            db_connection=self.db_connection,
            logger=self.logger
        )

        # Response Messages
        self.count_zero_response_message = "No More Requests Left"

    async def execute(self) -> Optional[str]:
        """
        Executes the prompt based on the provided tag and request data.

        Returns:
            Optional[str]: 
                The file path of the generated PDF document or None if no requests left.
        """

        # Initialize the user ID and IP address
        user_id: Optional[str] = None
        ip_address: Optional[str] = None

        # Generate Request Hash
        request_id: str = await self._get_request_hash()

        # Check if the request has already been executed
        previous_request: Requests = await self.db_service.get_request_by_request_id(
            request_id=request_id
        )

        # If the request has already been executed, return the file path
        if previous_request:

            # Get the file path from the previous request
            file_path = await self.db_service.get_pdf_file_path_by_pdf_id(
                pdf_id=previous_request.pdf_id)

            return file_path

        # Flag to check if user is logged in
        is_user_logged_in = self.jwt_token is not None

        # Check Capacity for User or IP
        if not is_user_logged_in:
            ip_address = self.request.client.host
            count = await self._execute_for_ip(ip_address)

        else:
            # Get User ID from JWT Token
            user_id = await self.jwt_lib.get_user_id_from_jwt(token=self.jwt_token)

            count = await self._execute_for_user(user_id=user_id)

        # If count is None, it means no more requests left
        if count is None:
            return JSONResponse(
                content={"message": self.count_zero_response_message},
                status_code=403
            )

        # Execute the prompt
        file_path: str = await self._execute_sql_prompt()

        # Update Database with the executed prompt

        # Update Count for User or IP
        if is_user_logged_in:
            await self.db_service.update_count_for_user(
                user_id=user_id,
                new_count=count - 1
            )
        else:
            await self.db_service.update_count_for_ip(
                ip_address=self.request.client.host,
                new_count=count - 1
            )

        # Update Database
        await self._update_database_after_execution(
            file_path=file_path,
            request_id=request_id,
            user_id=user_id,
            ip_address=ip_address
            )

        # Return the file path
        return file_path

    async def _execute_for_ip(self, ip_address: str) -> Optional[int]:
        """
        Executes the prompt for a user based on their IP address.

        Args:
            ip_address (str): The IP address of the user.

        Returns:
            Optional[int]: The count of requests left for the user based on their IP address.
        """

        # Check Count for IP Address
        count = await self.db_service.get_count_for_ip(ip_address=ip_address)

        # If count is None, it means the IP is new or not found
        if count is None:

            # New IP, insert into database
            count = await self.db_service.inset_new_ip(ip_address=ip_address)

        # If count is 0, return the zero response message
        elif count == 0:

            # No more requests left for this IP
            return None

        return count

    async def _execute_for_user(self, user_id: str) -> Optional[int]:
        """
        Executes the prompt for a logged-in user.
        Args:
            user_id (str): The ID of the user.
        Returns:
            str: The response from executing the prompt.
        """
        # User is logged in, check user count
        count = await self.db_service.get_count_for_user(user_id=user_id)

        # If count is None, it means the user is new or not found
        if count is None:

            # New User, insert into database
            count = await self.db_service.insert_new_user(user_id=user_id)

        elif count == 0:

            # No more requests left for this user
            return None

        return count

    async def _execute_sql_prompt(self) -> str:
        """
        Executes the SQL prompt based on the provided tag and request data.

        Returns:
            str: The file path of the generated PDF document.
        """
        # Create an instance of Prompt with the provided tag
        prompt_instance = await Prompt.create(tag=self.tag)

        # Execute the prompt with the provided request JSON
        file_path: str = await prompt_instance.execute_prompt(
            sql_script=self.sql_script,
            business=self.business_name
        )

        return file_path

    async def _get_request_hash(self) -> str:
        """
        Generates a unique hash for the request based on the SQL script and business name.

        Returns:
            str: The unique hash for the request.
        """
        # Create a unique string based on the SQL script and business name
        unique_string = f"{self.sql_script}|||{self.business_name}"

        # Generate a SHA-256 hash of the unique string
        request_hash = hashlib.sha256(unique_string.encode()).hexdigest()

        return request_hash

    async def create_sql_script_file_path(
            self,
            business_name: str,
            sql_script: str,
            request_id: str
        ) -> str:
        """
        Creates a file path for the SQL script based on the business name and SQL script.
        Args:
            business_name (str): The name of the business.
            sql_script (str): The SQL script to be executed.
        Returns:
            str: The file path for the SQL script.
        """
        # Create the file path
        file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "sql_scripts",
            f"{business_name}_{request_id}.sql")

        with open(file_path, 'w', encoding="utf-8") as file:
            file.write(sql_script)

        return file_path


    async def _update_database_after_execution(
            self,
            file_path: str,
            request_id: str,
            user_id: Optional[str] = None,
            ip_address: Optional[str] = None
        ) -> None:
        """
        Updates the database with the executed prompt details.

        Args:
            file_path (str): The file path of the generated PDF document.
            request_id (str): The unique identifier for the request.
            user_id (Optional[str], optional): 
                The ID of the user who made the request. Defaults to None.
            ip_address (Optional[str], optional): 
                The IP address of the user who made the request. Defaults to None.
        """
        # Get Business ID from Business Name
        business_id = await self.db_service.get_business_id_from_business_name(
            business_name=self.business_name
        )

        sql_script_file_path = await self.create_sql_script_file_path(
            business_name=self.business_name,
            sql_script=self.sql_script,
            request_id=request_id
        )

        # Update SQL Table with the executed SQL script
        sql_id = await self.db_service.insert_sql_script(
            sql_script_path=sql_script_file_path,
            business_id=business_id
        )

        # Update PDF Table with the new document
        pdf_id = await self.db_service.insert_pdf_file(
            file_path=file_path,
            sql_id=sql_id
        )

        # Update Requests Table with the new request
        await self.db_service.insert_new_request(
            request_id=request_id,
            user_id=user_id,
            ip_address=ip_address,
            pdf_id=pdf_id
        )

        # Update the count for the user or IP address
        if user_id:
            await self.db_service.update_count_for_user(
                user_id=user_id,
                new_count=await self.db_service.get_count_for_user(user_id=user_id) - 1
            )
        else:
            await self.db_service.update_count_for_ip(
                ip_address=ip_address,
                new_count=await self.db_service.get_count_for_ip(ip_address=ip_address) - 1
            )

        # Log the successful execution
        self.logger.info("Updated Database...")
        self.logger.debug(f"File Path: {file_path}")
        self.logger.debug(f"Request ID: {request_id}")
        self.logger.debug(f"User ID: {user_id}")
        self.logger.debug(f"IP Address: {ip_address}")
        self.logger.debug(f"Business ID: {business_id}")
            