"""
Utility functions for JWT authentication.
This module provides functions to create and decode JSON Web Tokens (JWT) using the HS256 algorithm.
It uses a secret key from environment variables or a default value for signing and verifying tokens.
Constants:
    SECRET_KEY (str): Secret key used for encoding and decoding JWTs.
    ALGORITHM (str): Algorithm used for JWT encoding/decoding (default: "HS256").
    ACCESS_TOKEN_EXPIRE_MINUTES (int): Token expiration time in minutes (default: 60).
Functions:
    create_jwt(data: dict) -> str:
        Generates a JWT token with the provided data and expiration time.
        Args:
            data (dict): The payload to encode in the JWT.
        Returns:
            str: The encoded JWT token.
    decode_jwt(token: str) -> dict or None:
        Decodes and verifies a JWT token.
        Args:
            token (str): The JWT token to decode.
        Returns:
            dict: The decoded payload if the token is valid.
            None: If the token is invalid or expired.
"""
from datetime import datetime, timedelta, timezone
import os
from typing import Optional
from jose import JWTError, jwt
from core.generate_id import GenerateId
from core.custom_logger import CustomLogger

class JWTLibrary:
    """
    AuthLibrary provides methods for creating and decoding
    JSON Web Tokens (JWT) for authentication purposes.
    It manages token generation with expiration
    and secure encoding/decoding using a configurable secret key and algorithm.    
    """
    def __init__(self, logger: CustomLogger = CustomLogger()):
        self._secret_key = os.getenv("JWT_SECRET_KEY")
        self._algorithm = "HS256"
        self._access_token_expire_minutes = 60
        self._generate_user_id_obj = GenerateId()
        self._logger = logger

    async def create_jwt(self, data: dict) -> str:
        """
        Generates a JSON Web Token (JWT) containing the provided data and an expiration time.
        This function copies the input data,
        adds an expiration timestamp,
        and encodes it into a JWT using the specified secret key and algorithm.
            data (dict): The payload data to include in the JWT.
            str: The encoded JWT as a string.
        Raises:
            Exception: If encoding fails due to invalid input or configuration.
        Function Comments:
            - Copies the input data to avoid mutation.
            - Sets the expiration time based on ACCESS_TOKEN_EXPIRE_MINUTES.
            - Uses SECRET_KEY and ALGORITHM for encoding.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self._access_token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)

    async def decode_jwt(self, token: Optional[str]) -> Optional[dict]:
        """
        Decodes a JWT token using the specified secret key and algorithm.
            token (str): The JWT token string to decode.
            dict or None: The decoded payload as a dictionary if successful,
                otherwise None if decoding fails.
        Raises:
            None: Any JWT decoding errors are caught and result in None being returned.
        """
        if token is None:
            return token
        try:
            return jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
        except JWTError:
            return None

    async def generate_jwt_token_schema(self, token: dict, user:dict, tag: str) -> dict:
        """
        Generate Schema of JWT Token from token, user, and oauth tag

        Args:
            token (dict): Token Information
            user (dict): User Information derived from token
            tag (str): OAuth Tag (Google, Outlook, Github)

        Returns:
            dict: Map of JWT Schema
        """
        # Fetching User Information
        user_name = user.get("name", None)
        user_email = user.get("email", None)

        # Generating User ID
        user_id = self._generate_user_id_obj.generate_user_id(
            name=user_name,
            email=user_email
        )
        # Generating Token Schema
        token_dict_schema = {
            "token": dict(token),
            "user": dict(user),
            "name": user_name,
            "email": user_email,
            "user_id": user_id,
            "oauth_tag": tag
        }

        # Returning the Schema
        return token_dict_schema

    async def generate_jwt_from_token(self, token: dict, user: dict, tag: str) -> str:
        """
        Generating JWT token from token, user, and oauth tag

        Args:
            token (dict): Token Information
            user (dict): User Information Derived from Token
            tag (str): OAuth Tag (Outlook, Google, Github)

        Returns:
            str: JWT Encoded String
        """
        return await self.create_jwt(data=await self.generate_jwt_token_schema(
            token=token,
            user=user,
            tag=tag
        ))
