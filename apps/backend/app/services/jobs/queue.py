from celery import Celery
from app.core.config import settings

# Initialize client connection to Redis queue
celery_app = Celery("ocr_workers", broker=settings.REDIS_URL)

class JobQueueService:
    def dispatch_processing_job(self, job_id: str, file_key: str):
        """Enqueues a processing job for the worker pipeline."""
        # Task name MUST match what workers are listening for exactly
        return celery_app.send_task(
            "src.main.process_ocr_document",
            args=[job_id, file_key],
            queue="ocr_processing"
        )

job_queue_service = JobQueueService()
