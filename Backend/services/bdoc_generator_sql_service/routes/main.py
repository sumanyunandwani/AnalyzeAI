# ----------------------------- Importing Required Libraries -----------------------------
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from core.request_validation import RequestValidation
from core.prompt_wrapper import PromptWrapper
from core.database_connection import AsyncSQLAlchemySingleton
from core.custom_logger import CustomLogger
from core.database_wrapper import DatabaseWrapper


# ----------------------------- Initializing the environment -----------------------------
# Startup and shutdown events for the FastAPI application
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event to initialize the database connection and create schema if not exists.
    """
    db = AsyncSQLAlchemySingleton()
    db.init_engine()
    await db.create_schema_if_not_exists()
    await db.seed_business_domains()
    app.state.db = db
    yield
    # NOTE: Cleanup can be added here if needed

# Initialize the logger
logger = CustomLogger.setup_logger(__name__)

# Initialize the FastAPI application
app = FastAPI(lifespan=lifespan)

# Initialize the session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key = "s3cr3t-key-1234567890",
    same_site = "lax",
    # https_only = True # NOTE: Turn it on in Production
)

# CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Stripe for payments
stripe_api_key = "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"
stripe_publishable_key = "pk_live_51RqLPxGWg8H1CYMicNbnuZiNm6pV9kGWBZkX94cWol0bm04WlfziffK2d0hIyfpYACjRH6iuooO1qZ2nJT9bvffH00qdmibrJr"

# Initiate Validation Utility
request_validator = RequestValidation(logger=logger)

# ----------------------------- API Endpoints -----------------------------
# Endpoint to execute a prompt based on the provided tag
@app.post("/prompt/{tag}")
async def execute_prompt(tag: str, request: Request = None) -> FileResponse:
    """
    Execute a prompt based on the provided tag and text.
    
    Args:
        tag (str): The tag associated with the prompt.
        text (str): The text to be used in the prompt execution.
    
    Returns:
        str: The response from executing the prompt.
    """
    # Wait for the request JSON to be available
    request_json = await request.json()

    # Log the tag and request JSON
    logger.debug(f"Executing prompt for tag: {tag}")
    logger.debug(f"Request JSON: {request_json}")

    # Validate Request
    await request_validator.validate_request(
        request=request_json,
        required_keys=[
            "script",
            "business"
        ])

    # Validate Count
    jwt_token = request.cookies.get("access_token", None)

    prompt_service = PromptWrapper(
        tag=tag,
        request=request,
        request_json=request_json,
        jwt_token=jwt_token,
        db_connection=app.state.db,
        logger=logger)

    file_path: str = await prompt_service.execute()

    # Log the file path of the generated PDF
    logger.debug(f"Generated PDF file path: {file_path}")

    # Return the reponse if not file path
    if not isinstance(file_path, str):
        return file_path

    # Return the response
    return FileResponse(
        path=file_path,
        media_type='application/pdf',
        filename='bdoc.pdf')

@app.put("/update/user/count/{count}")
async def update_user_count(count: int, request: Request) -> JSONResponse:
    """
    Update the user count based on the provided count.
    Args:
        count (int): The count to be updated.
        request (Request): The request object containing user information.
    Returns:
        JSONResponse: A response indicating the success or failure of the operation.
    """
    # Validate the request
    request_validator.validate_request(
        request=request,
        required_keys=["acess_token"]
    )

    # Initialize the DatabaseWrapper
    db_wrapper = DatabaseWrapper(
        db_connection=app.state.db,
        logger=logger
    )

    # Update the count for the user
    success = await db_wrapper.update_count_for_user_from_request(
        request=request,
        new_count=count
    )

    # Return the response
    return JSONResponse(
        content={"success": success, "message": "User count updated successfully."},
        status_code=200
    )
