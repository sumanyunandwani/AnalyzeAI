"""
This module provides an OAuthService class that handles OAuth authentication
for various providers such as Google, GitHub, and Outlook.
It includes methods for initiating the OAuth flow, handling callbacks,
and refreshing tokens when necessary.
"""
import os
from datetime import datetime, timezone
from logging import Logger
from typing import Tuple
from authlib.integrations.starlette_client import OAuth
from starlette.datastructures import URL
from fastapi import Request, HTTPException
from .custom_logger import CustomLogger

class OAuthService:
    """
    OAuth Utility
    """
    def __init__(self, logger: Logger = CustomLogger.setup_logger(__name__)):
        self._accepted_oauth_tags = set(["google", "github", "outlook"])
        self._oauth_obj = OAuth()
        self._logger = logger

        self._register_oauth()

    def _register_oauth(self) -> None:

        # Register OAuth providers - Google
        self._oauth_obj.register(
            name="google",
            client_id=os.getenv("GOOGLE_CLIENT_ID"),
            client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={
                'scope': 'openid email profile',
                "prompt": "consent",
                "access_type": "offline",
                }
        )

        # Register OAuth providers - GitHub
        self._oauth_obj.register(
            name="github",
            client_id=os.getenv("GITHUB_CLIENT_ID"),
            client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
            access_token_url='https://github.com/login/oauth/access_token',
            authorize_url='https://github.com/login/oauth/authorize',
            api_base_url='https://api.github.com/',
            client_kwargs={
                'scope': 'user:email',
                }
        )

        # Register OAuth providers - Outlook
        self._oauth_obj.register(
            name='outlook',
            client_id=os.getenv("OUTLOOK_CLIENT_ID"),
            client_secret=os.getenv("OUTLOOK_CLIENT_SECRET"),
            authorize_url='https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
            access_token_url='https://login.microsoftonline.com/common/oauth2/v2.0/token',
            client_kwargs={
                'scope': 'openid email profile offline_access',
                'validate_iss': False
            },
            jwks_uri="https://login.microsoftonline.com/common/discovery/v2.0/keys"
        )

    async def get_oauth(self, tag: str, request: Request, redirect_uri: URL) -> None:
        """
        
        Initiates the OAuth authorization flow for the specified provider.
        This method redirects the user to the OAuth provider's authorization page
        based on the given tag. Supported providers are Google, GitHub, and Outlook.

        Args:
            tag (str): The OAuth provider identifier.
                Supported values are "google", "github", and "outlook".
            request (Request): The incoming HTTP request object.
            redirect_uri (URL): The URI to redirect to after authorization.

        Returns:
            None: This method performs a redirect and does not return a value.

        Raises:
            None explicitly, but may raise exceptions from the 
            underlying OAuth library if the tag is invalid
            or if authorization fails.
        """
        # Redirect to the OAuth provider's authorization page
        if tag == "google":
            return await self._oauth_obj.google.authorize_redirect(request, redirect_uri)
        elif tag == "github":
            return await self._oauth_obj.github.authorize_redirect(request, redirect_uri)
        elif tag == "outlook":
            return await self._oauth_obj.outlook.authorize_redirect(request, redirect_uri)

    async def callback_oauth(self, tag: str, request: Request) -> Tuple[dict, dict]:
        """
        Handles OAuth callback for different providers and retrieves user information.

        Args:
            tag (str): The OAuth provider identifier.
                Supported values are "google", "github", and "outlook".
            request (Request): The incoming request object containing OAuth callback data.

        Raises:
            Exception: If the OAuth provider is not supported or if authentication fails.

        Returns:
            Tuple[dict, dict]: A tuple containing the token dictionary
            and the user information dictionary.
        """
        # For different OAuth providers, handle the authentication
        # Check which OAuth provider is being used and handle accordingly
        # For Google and Outlook, user info is in the token['userinfo']
        # For GitHub, user info is fetched separately using the token
        # Returns both the token and user info as a tuple
        if tag == "google":
            token = await self._oauth_obj.google.authorize_access_token(request)
            user = token['userinfo']
        elif tag == "github":
            token = await self._oauth_obj.github.authorize_access_token(request)
            user = await self._oauth_obj.github.get('user', token=token)
            user = user.json()
        elif tag == "outlook":
            token = await self._oauth_obj.outlook.authorize_access_token(request)
            user = token['userinfo']
        return (token, user)

    async def refresh_token(self, tag: str, jwt_token: dict) -> Tuple[dict, dict]:
        """
        Refreshes the OAuth access token if it has expired.

        Args:
            tag (str): The OAuth provider tag (e.g., "google", "outlook").
            jwt_token (dict): A dictionary containing the current token and user information.

        Raises:
            HTTPException: If the token is expired and no refresh token is available.

        Returns:
            Tuple[dict, dict]: A tuple containing the refreshed token and user information.
        """

        token = jwt_token.get("token")
        user = jwt_token.get("user")

        # Check if the token is expired
        expires_at = token.get("expires_at")
        if expires_at and datetime.now(tz=timezone.utc).timestamp() > expires_at:

            # If the token is expired, refresh it based on the OAuth provider
            if "refresh_token" not in token:
                raise HTTPException(
                    status_code=401,
                    detail="Token expired and no refresh token available"
                )

            # Refresh the token based on the OAuth provider
            if tag == "google":
                token = await self._refresh_google_access_token(token)
                user = dict(token).get("userinfo")
            elif tag == "outlook":
                token = await self._refresh_outlook_access_token(token)
                user = dict(token).get("userinfo")

        return (token, user)

    async def _refresh_google_access_token(self, token: dict) -> dict:
        """
        Refresh the Google OAuth access token using the refresh token stored in the session.

        Args:
            request (Request): The incoming request object.

        Raises:
            HTTPException: If no refresh token is available in the session.

        Returns:
            dict: The new access token information.
        """

        # Check if the token and refresh token are available
        if not token or "refresh_token" not in token:
            raise HTTPException(status_code=401, detail="No refresh token available")

        # Generate a new access token using the refresh token
        new_token = await self._oauth_obj.google.refresh_token(
            url='https://oauth2.googleapis.com/token',
            refresh_token=token['refresh_token']
        )

        # Log the new token information
        self._logger.debug(f"New token: {new_token}")

        # Return the new token
        return new_token

    async def is_valid_oauth_tag(self, tag: str) -> bool:
        """
        Validate Oauth Tab by returning True False

        Args:
            tag (str): OAuth Tag

        Returns:
            bool: True in case of accpetance, False otherwise.
        """
        return tag in self._accepted_oauth_tags

    async def _refresh_outlook_access_token(self, token: dict) -> dict:
        """
        Refresh the Outlook OAuth access token using the refresh token stored in the session.

        Args:
            request (Request): The incoming request object.

        Raises:
            HTTPException: If no refresh token is available in the session.

        Returns:
            dict: The new access token information.
        """
        # Check if the token and refresh token are available
        if not token or "refresh_token" not in token:
            raise HTTPException(status_code=401, detail="No refresh token available")

        # Refresh token using Microsoft identity platform
        new_token = await self._oauth_obj.outlook.refresh_token(
            url='https://login.microsoftonline.com/common/oauth2/v2.0/token',
            refresh_token=token['refresh_token']
        )

        return new_token