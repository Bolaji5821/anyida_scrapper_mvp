from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

# Redis URL from env or default
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "anyida_scraper",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.tasks"] # Ensure tasks are loaded
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Africa/Lagos",
    enable_utc=True,
    task_track_started=True,
    worker_concurrency=2, # Limit concurrency for browser safety
    worker_max_tasks_per_child=10, # Restart worker after 10 tasks to prevent memory leaks (especially with browser)
)
