"""
This code is part of the AnalyzeAI project.
It is licensed under the Apache License, Version 2.0.
See the LICENSE file for more details.
"""
import logging
from pathlib import Path
from typing import List, Dict, Optional
from xhtml2pdf import pisa
from fastapi import HTTPException
from core.custom_logger import CustomLogger
from podels.get_podel import Podel, PodelNode
from core.prompt_executor import AsyncSingletonPromptExecutor

class Prompt:
    """
    This class is responsible for executing prompts based on a tag.
    It retrieves the prompt from the Podel based on the tag and executes it using
    the AsyncSingletonPromptExecutor.
    It ensures that the prompt execution is done asynchronously and allows for
    concurrent execution of multiple prompts without blocking the event loop.
    """
    def __init__(self, tag: str, logger: Optional[logging.Logger] = None) -> None:

        # File Counter
        self._file_counter = 0

        # Predefined tags for different prompts
        self._test_podel = "test_podel"
        self._sql_podel = "sql_podel"
        self._instagram_podel = "instagram_podel"

        # Dictionary to map tags to their respective Podels
        self._tags_dict: Dict[str, str] = {
            "test": self._test_podel, 
            "sql": self._sql_podel, 
            "instagram": self._instagram_podel
        }

        # Validate the tag
        self._validate_tag(tag)

        # Set the tag for the prompt
        self.tag = self._tags_dict[tag]

        # Initialize the PodelNode and AsyncSingletonPromptExecutor
        self._podel_node: Optional[PodelNode] = None
        self._executor: Optional[AsyncSingletonPromptExecutor] = None

        # Initialize the logger
        self.logger = logger or CustomLogger.setup_logger(__name__)

    @classmethod
    async def create(cls, tag: str) -> 'Prompt':
        """
        Asynchronous factory method to create an instance of Prompt.
        This method initializes the Podel instance and the AsyncSingletonPromptExecutor

        Args:
            tag (str): The tag associated with the prompt.

        Raises:
            ValueError: If the tag is not valid or does not exist in the predefined set.

        Returns:
            Prompt: An instance of the Prompt class initialized with the specified tag.
        """
        self = cls(tag)

        # Get the singleton instance of Podel
        podel_instance: Podel = await Podel.get_instance()
        self._podel_node = podel_instance.get_podel(tag=self.tag)

        # Ensure that the PodelNode is not None
        if not self._podel_node:
            raise ValueError(f"No prompt found for tag: {self.tag}")

        # Initialize the AsyncSingletonPromptExecutor
        self._executor = AsyncSingletonPromptExecutor()
        await self._executor.init(max_concurrent_calls=1)

        # Return the initialized instance
        return self

    def _validate_tag(self, tag: str) -> None:
        """
        Validates the tag to ensure it is a non-empty string and exists in the predefined set.

        Args:
            tag (str): The tag to validate.

        Raises:
            ValueError: If the tag is not a non-empty string 
            or does not exist in the predefined set.
        """
        # Ensure the tag is a non-empty string and exists in the predefined set
        if not isinstance(tag, str) or not tag or tag not in self._tags_dict:
            raise ValueError("Tag must be a non-empty string.")

    async def _convert_response_to_pdf(self, response: str) -> str:
        """
        Converts the response string to a PDF file.
        
        Args:
            response (str): The response string to be converted to PDF.
        
        Returns:
            str: The file path of the created PDF file.
        """
        # Generate a unique file name based on the file counter
        file_path = Path(__file__).parent.parent.joinpath(
            'pdfs',
            f"sql_to_business_bdoc_{self._file_counter}.pdf"
        )

        # Increment the file counter for the next file
        self._file_counter += 1

        # Write the response to a PDF file
        with open(file_path, 'w+b') as pdf_file:

            # Convert the response HTML to PDF
            pisa.CreatePDF(
                src=response,
                dest=pdf_file
            )

        # Log the file creation
        self.logger.info(f"PDF file created at: {file_path}")

        # Return the file path
        return str(file_path)

    async def execute_prompt(self, sql_script: str, business: str) -> bool:
        """
        Executes the prompt associated with the tag.
        This method retrieves the prompt from the Podel based on the tag
        and executes it using the AsyncSingletonPromptExecutor.
        It ensures that the prompt execution is done asynchronously and allows for
        concurrent execution of multiple prompts without blocking the event loop.
        
        Args:
            input_dict (Dict[str, str]): A dictionary containing the input parameters
                required for executing the prompt, such as 'sql_script' and 'business'.

        Raises:
            ValueError: If the tag is not supported or if the input_dict does not contain
                the required parameters for the prompt execution.

        Returns:
            bool: True if the prompt execution was successful, False otherwise.
        """
        # Switch based on the tag to determine which prompt to execute

        # For SQL Podel
        if self.tag == self._sql_podel:

            # Initialize SQLPrompt with the PodelNode and executor
            sql_prompt_obj = SQLPrompt(
                podel_node=self._podel_node,
                executor=self._executor,
                logger=self.logger
            )

            # Execute the SQL prompt with the provided input parameters
            response: str = await sql_prompt_obj.execute_prompt_sql(
                sql_script=sql_script,
                business=business
            )

            # Create a pdf file from the response
            file_path: str = await self._convert_response_to_pdf(response)

            # Log the file creation
            self.logger.info(f"PDF file created at: {file_path}")

            # Return the file path as a response
            return file_path

        # For Test Podel
        elif self.tag == self._test_podel:
            # Implement test prompt execution logic here
            pass

        # For Instagram Podel
        elif self.tag == self._instagram_podel:
            # Implement Instagram prompt execution logic here
            pass

        # If the tag is not recognized, raise an error
        else:
            raise ValueError(f"Unsupported tag: {self.tag}")

        return True

class SQLPrompt():
    """
    This class is responsible for executing SQL prompts.
    It retrieves the prompt from the Podel based on the tag and executes it using
    the AsyncSingletonPromptExecutor.
    It ensures that the prompt execution is done asynchronously and allows for
    concurrent execution of multiple prompts without blocking the event loop.
    """
    def __init__(
            self,
            podel_node: Prompt,
            executor: Optional[AsyncSingletonPromptExecutor] = None,
            logger: Optional[logging.Logger] = None) -> None:
        self._podel_node = podel_node
        self.logger = logger or CustomLogger.setup_logger(__name__)
        self._executor = executor

    async def execute_prompt_sql(self, sql_script: str = None, business: str = None) -> str:
        """
        Executes the prompt associated with the tag.
        This method retrieves the prompt from the Podel based on the tag
        and executes it using the AsyncSingletonPromptExecutor.
        
        Returns:
            str: The response from executing the prompt.
        """
        # Start with the head of the Podel linked list
        _head: PodelNode = self._podel_node

        # Initialize chat history and response
        chat_history: Optional[List[Dict[str, str]]] = None
        response = ""

        # Iterate through the linked list of prompts
        while _head:

            # Log the current prompt and its parameters
            self.logger.debug(f"History: {chat_history}")
            self.logger.debug(f"SQL Script: {sql_script}")
            self.logger.debug(f"Business: {business}")
            self.logger.debug(f"Need answer: {_head.need_answer}")
            self.logger.debug(f"Error Message Dict: {_head.error_message_dict}")
            self.logger.info(f"Executing prompt: {_head.prompt}")

            # Execute the prompt using the executor
            response, chat_history = await self._executor.execute_prompt(
                    prompt=_head.prompt.format(sql_script=sql_script, business=business),
                    chat_history=None if not _head.need_history else chat_history
                )

            # Log the response
            self.logger.info(f"Response: {response}")

            # Check if the prompt requires an answer and if it is present in the response
            if _head.need_answer:
                if _head.need_answer not in response:
                    self.logger.error(
                        f"Expected answer '{_head.need_answer}' not found in response: {response}")
                    raise HTTPException(
                        status_code=_head.error_message_dict["status_code"],
                        detail=_head.error_message_dict["message"])
                self.logger.info(
                    f"Expected answer '{_head.need_answer}' found in response: {response}")

            # Move to the next node in the linked list
            _head = _head.next

        # Return the final response after executing all prompts
        return response
