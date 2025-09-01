"""
This module sets up the FastAPI application for user authentication using OAuth providers
like Google, GitHub, and Outlook. It includes endpoints for login and authentication,
middleware for session management and CORS, and integrates JWT for secure token handling.
"""
# ----------------------------- Importing Required Libraries -----------------------------
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from core.custom_logger import CustomLogger
from core.generate_id import GenerateId
from core.database_connection import AsyncSQLAlchemySingleton
from core.jwt_lib import JWTLibrary
from core.oauth_service import OAuthService

# ----------------------------- Initializing the environment -----------------------------
# Startup and shutdown events for the FastAPI application
@asynccontextmanager
async def lifespan(app_object: FastAPI):
    """
    Lifespan event to initialize the database connection and create schema if not exists.
    """
    db = AsyncSQLAlchemySingleton()
    db.init_engine()
    await db.create_schema_if_not_exists()
    app_object.state.db = db
    yield
    # NOTE: Cleanup can be added here if needed

# Initialize the logger
logger = CustomLogger.setup_logger(__name__)

# Initialize the FastAPI application
app = FastAPI(lifespan=lifespan)

# Initialize the session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key = os.getenv("SESSION_SECRET"),
    same_site = "lax"
    # https_only = True # NOTE: Turn it on in Production
)

# CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the oauth client
oauth_service = OAuthService(logger=logger)

# Initiate Auth Library
jwt_auth = JWTLibrary(logger=logger)

# Initiate User ID Utility
generate_user_id_utility = GenerateId(logger=logger)

# ----------------------------- API Endpoints -----------------------------
# Endpoint to handle OAuth login
@app.get("/login/{tag}")
async def login(tag: str, request: Request):
    """
    Redirect the user to the Google OAuth login page.
    
    Args:
        request (Request): The incoming request object.
    
    Returns:
        RedirectResponse: A redirect to the Google OAuth login page.
    """
    # Validate the tag
    if not await oauth_service.is_valid_oauth_tag(tag=tag):
        raise HTTPException(status_code=400, detail="Invalid OAuth provider tag")

    # Log the login attempt
    logger.debug("Login request received")
    logger.debug(f"Request: {request}")

    # Generate the redirect URI
    redirect_uri = request.url_for('auth', tag=tag)

    # Log the redirect URI
    logger.debug(f"Redirect URI: {redirect_uri}")

    return await oauth_service.get_oauth(
        tag=tag,
        request=request,
        redirect_uri=redirect_uri)

# Endpoint to handle OAuth authentication callback
@app.get("/auth/{tag}")
async def auth(tag: str, request: Request, response: Response):
    """
    Authenticate the user using Google OAuth.
    
    Args:
        request (Request): The incoming request object.
    
    Returns:
        JSONResponse: A response indicating the authentication status.
    """
    # Log the authentication attempt
    logger.debug("Authentication request received")

    token, user = await oauth_service.callback_oauth(tag=tag, request=request)

    # Log the token and user information
    logger.debug(f"token: {token}")
    logger.debug(f"User authenticated: {dict(user)}")

    # Setting JWT Token in cookies
    redirect_response = RedirectResponse(
        url=os.getenv("REDIRECT_URL_AFTER_OAUTH"),
        status_code=307
    )

    # JWT Token generation and setting in cookies
    cookie = await jwt_auth.generate_jwt_from_token(
            token=token,
            user=user,
            tag=tag
        )

    redirect_response.set_cookie(
        key="access_token",
        value=cookie,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/"
    )

    # Log the response cookie
    logger.debug(f"Response cookie set: {cookie}")


    # Database Entry for User
    await generate_user_id_utility.create_user(
        name=user.get("name"),
        email=user.get("email"),
        db_connection=app.state.db
    )

    return redirect_response

# Endpoint to handle status calls on start
@app.get("/status")
async def get_status(request: Request):
    """
    Send Name and Email Details if Logged In

    Args:
        request (Request): Request Object

    Raises:
        HTTPException: 401 error due to no authentication
        HTTPException: 400 error due to invalid JWT access token
        HTTPException: 403 error due to invalid or expired token

    Returns:
        JSONResponse: Send JSON with name and email keys
    """
    token = request.cookies.get("access_token")
    if not token:
        logger.warning("No Access Token found in requests!")
        return JSONResponse({"name": "Guest"})

    try:
        payload = await jwt_auth.decode_jwt(token)
        name = payload.get("name")
        email = payload.get("email")
        if not name or not email:
            logger.warning(f"Name: {name} or email: {email} missing!")
            return JSONResponse({"name": name or "Guest"})
        logger.debug(f"Extracted Name: {name} and Email: {email} from access token")
        return JSONResponse({"name": name, "email": email})
    except Exception as e:
        logger.error(f"JWT decode error: {e}")
        return JSONResponse({"name": "Guest"})
