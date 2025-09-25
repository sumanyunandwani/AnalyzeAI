"""
This module defines a Celery task for executing long-running prompt operations asynchronously.
"""
from celery import shared_task
from core.prompt_wrapper import PromptWrapper
from core.database_connection import AsyncSQLAlchemySingleton
from core.custom_logger import CustomLogger

logger = CustomLogger.setup_logger(__name__)

@shared_task(bind=True)
def execute_prompt_task(
    tag: str,
    request_json: dict,
    jwt_token: str | None,
    db_connection: AsyncSQLAlchemySingleton
    ) -> dict:
    """
    Run long-running prompt execution in Celery worker.
    """
    try:

        prompt_service = PromptWrapper(
            tag=tag,
            request=None,
            request_json=request_json,
            jwt_token=jwt_token,
            db_connection=db_connection,
            logger=logger
        )

        file_path = prompt_service.execute_sync() # Celery expects sync call

        return {"status": "completed", "file_path": file_path}

    except Exception as e:
        logger.error("Task failed: %s", e)
        return {"status": "failed", "error": str(e)}
