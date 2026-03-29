import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Celery App Initialization
app = Celery("ocr_workers", broker=REDIS_URL, backend=REDIS_URL)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Explicitly discover tasks to avoid circular imports during worker startup
from .tasks.extraction_task import process_ocr_document