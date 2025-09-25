"""
This module contains the main FastAPI application for handling prompt execution,
user count updates, and retrieving business names.
"""
# ----------------------------- Importing Required Libraries -----------------------------
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from core.request_validation import RequestValidation
from celery_task.celery_app import celery_app
from celery.result import AsyncResult
from celery.exceptions import CeleryError
from core.database_connection import AsyncSQLAlchemySingleton
from core.custom_logger import CustomLogger
from core.database_wrapper import DatabaseWrapper
from celery_task.task import execute_prompt_task


# ----------------------------- Initializing the environment -----------------------------
# Startup and shutdown events for the FastAPI application
@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """
    Lifespan event to initialize the database connection and create schema if not exists.
    """
    db = AsyncSQLAlchemySingleton()
    db.init_engine()
    await db.create_schema_if_not_exists()
    await db.seed_business_domains()
    fastapi_app.state.db = db
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

# Initiate Validation Utility
request_validator = RequestValidation(logger=logger)

# ----------------------------- API Endpoints -----------------------------
# Endpoint to execute a prompt based on the provided tag
@app.post("/prompt/{tag}")
async def enqueue_prompt(tag: str, request: Request = None) -> JSONResponse:
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

    try:
        task = execute_prompt_task.delay(
            tag,
            request_json,
            jwt_token,
            app.state.db
        )
        return JSONResponse({
            "task_id": task.id,
            "status": "queued"
        })

    except (CeleryError, ValueError, RuntimeError) as e:
        logger.error(f"Celery error enqueueing task: {e}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

# Endpoint to update the user count
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
    # Awaiting the request JSON
    await request.json()

    # Validate the request
    await request_validator.validate_request(
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


@app.get("/task/{task_id}")
async def get_task_status(task_id: str) -> JSONResponse:
    """
    Get the status of a Celery task by its ID.

    Args:
        task_id (str): The ID of the Celery task.

    Returns:
        JSONResponse: A JSON response containing the task status and result if available.
    """
    result = AsyncResult(task_id, app=celery_app)
    if result.state == "PENDING":
        return JSONResponse({"task_id": task_id, "status": "pending"})
    elif result.state == "SUCCESS":
        return JSONResponse({
            "task_id": task_id,
            "status": "completed",
            "result": result.result
        })
    elif result.state == "FAILURE":
        return JSONResponse({
            "task_id": task_id,
            "status": "failed",
            "error": str(result.result)
        })
    return JSONResponse({"task_id": task_id, "status": result.state})

# Endpoint to get all the business names
@app.get("/business/names")
async def get_all_business_names() -> JSONResponse:
    """
    Retrieve all Supporting Business Names from the database.

    Returns:
        JSONResponse: JSON with key names and value list of business names
    """
    # Initialize the DatabaseWrapper
    db_wrapper = DatabaseWrapper(
        db_connection=app.state.db,
        logger=logger
    )

    # Return JSON Response where names is the key
    return JSONResponse(
        {
            "names": await db_wrapper.get_all_business()
        }
    )
