from arq import create_pool
from arq.connections import RedisSettings
from app.core.config import settings

class JobQueueService:
    @property
    async def _redis_pool(self):
        """Lazy initialization of Arq connection pool."""
        return await create_pool(RedisSettings(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT
        ))

    async def dispatch_processing_job(self, job_id: str, file_key: str):
        """Enqueues a processing job for the async worker pipeline."""
        pool = await self._redis_pool
        return await pool.enqueue_job(
            "process_ocr_document",
            job_id,
            file_key
        )

job_queue_service = JobQueueService()
