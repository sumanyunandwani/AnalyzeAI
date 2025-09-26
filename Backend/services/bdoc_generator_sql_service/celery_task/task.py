"""
This module defines a Celery task for executing long-running prompt operations asynchronously.
"""
from celery_task.celery_app import celery_app
from core.prompt_wrapper import PromptWrapper
from core.custom_logger import CustomLogger

logger = CustomLogger.setup_logger(__name__)

@celery_app.task(name="celery_task.task.execute_prompt_task", bind=True)
def execute_prompt_task(
        _,
        tag: str,
        request_json: dict[str, str],
        jwt_token: str | None,
        ip_address: str | None = None
    ) -> dict:
    """
    Run long-running prompt execution in Celery worker.
    """
    try:

        prompt_service = PromptWrapper(
            tag=tag,
            ip_address=ip_address,
            request_json=request_json,
            jwt_token=jwt_token,
            logger=logger
        )

        file_path = prompt_service.execute_sync() # Celery expects sync call

        return {"status": "completed", "file_path": file_path}

    except Exception as e:
        logger.error("Task failed: %s", e)
        return {"status": "failed", "error": str(e)}
