"""
This module defines the DatabaseWrapper class to manage database interactions.
It provides methods to check user
or IP address counts and update the database after prompt execution.
"""
from typing import Optional
from logging import Logger
from core.jwt_lib import JWTLibrary
from core.db_service import DBService
from core.database_connection import AsyncSQLAlchemySingleton
from core.custom_logger import CustomLogger
from fastapi import Request, HTTPException

class DatabaseWrapper:
    """
    DatabaseWrapper class provides methods to interact with the database.
    It includes methods for checking user
    or IP address counts and updating the database after prompt execution.
    Usage:
        db_wrapper = DatabaseWrapper(db_connection, logger)
        count = await db_wrapper.get_count_for_user(user_id)
        await db_wrapper.update_database_after_execution(file_path, request_id, user_id)
    """
    def __init__(
            self,
            db_connection: AsyncSQLAlchemySingleton,
            logger: Optional[Logger] = CustomLogger.setup_logger(__name__)
        ):
        self._db = db_connection
        self.logger = logger
        self.jwt_lib = JWTLibrary(logger=self.logger)
        self.db_service = DBService(db_connection=self._db, logger=self.logger)

    async def update_count_for_user_from_request(
            self,
            request: Request,
            new_count: int) -> bool:
        """
        Updates the count for a user based on the request data.
        Args:
            request (Request): The request object containing user information.
            new_count (int): The new count to be set for the user.
        Returns:
            bool: True if the count was updated successfully, False otherwise.
        """
        # Validate the request
        if not request.cookies.get("access_token"):
            raise HTTPException(status_code=401, detail="Unauthorized: No access token provided.")

        # Get the user ID from the JWT token in the request cookies
        user_id = self.jwt_lib.get_user_id_from_jwt(token=request.cookies.get("access_token"))

        # Validate the user ID
        await self.db_service.update_count_for_user(
            user_id=user_id,
            new_count=new_count
        )

        # Log the update
        self.logger.debug(f"Updated count for user {user_id} to {new_count}")

        return True
