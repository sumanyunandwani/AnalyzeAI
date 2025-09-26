"""
Celery application setup for asynchronous task processing using Redis as broker and backend.
"""
import os
from celery import Celery

celery_app = Celery(
    "worker",
    broker=os.getenv("REDIS_URL"),   # change for your environment
    backend=os.getenv("REDIS_URL"),
    include=["celery_task.task"]  # Ensure tasks are discovered
)

celery_app.conf.task_routes = {
    "celery_task.task.execute_prompt_task": {"queue": "prompts"},
}
