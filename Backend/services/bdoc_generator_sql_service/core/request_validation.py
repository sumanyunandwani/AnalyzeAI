"""
This module defines the RequestValidation class,
which provides functionality to validate incoming request objects.
It ensures that all required keys are present in a request, logging verification for each key
and raising an HTTPException if any required key is missing.
"""
from logging import Logger
from fastapi import Request, HTTPException
from .custom_logger import CustomLogger

class RequestValidation:
    """
    RequestValidation is a utility class for validating incoming request objects.
    This class provides methods to ensure that all required keys are present in a request,
    logging verification for each key and raising an HTTPException if any required key is missing.
    Attributes:
        _logger (Logger): Logger instance used for logging validation steps.
    Methods:
        __init__(logger: Logger = CustomLogger.setup_logger())
            Initializes the RequestValidation instance with a logger.
        async validate_request(request: Request, required_keys: list[str] = []) -> bool
    """
    def __init__(self, logger: Logger = CustomLogger()) -> None:
        self._logger = logger

    async def validate_request(self, request: Request, required_keys: list[str]) -> bool:
        """
        Validates that all required keys are present in the incoming request.
        Iterates through the provided list of required keys and checks
        if each key exists in the request object.
        If any required key is missing, raises an HTTPException with status code 422.
        Logs verification for each key found.

        Args:
            request (Request): The incoming request object to validate.
            required_keys (list[str], optional): 
                List of keys that must be present in the request. Defaults to [].

        Raises:
            HTTPException: If any required key is missing from the request.

        Returns:
            bool: True if all required keys are present.
        """
        for key in required_keys:
            if key not in request:
                raise HTTPException(status_code=422, detail=f"Missing or null key: {key}")
            self._logger.debug(f"Verified that key: {key} exists in Requests")
        return True
