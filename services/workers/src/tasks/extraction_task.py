from ..main import app as celery_app
from ..repositories.job_repository import JobRepository
from ..repositories.result_repository import ResultRepository
from ..pipelines.extraction_pipeline import ExtractionPipeline
from ..exceptions.pipeline import PipelineError
import logging
import sys

# Core worker logger using structured JSON formatter
logger = logging.getLogger("worker")

@celery_app.task(name="src.main.process_ocr_document", bind=True, max_retries=3)
def process_ocr_document(self, job_id: str):
    """
    Bulletproof Celery orchestrator:
    1. Idempotency Check
    2. Atomic Status Update
    3. Pipeline execution with Stage-level Fallbacks
    4. Independent result persistence.
    """
    job_repo = JobRepository()
    result_repo = ResultRepository()
    pipeline = ExtractionPipeline()
    log_extra = {"job_id": job_id}

    try:
        # 1. Fetch metadata & state safety
        job = job_repo.get_job_status(job_id)
        if not job:
            logger.error(f"Job {job_id} not found in repository.", extra=log_extra)
            return

        if job.status == "completed":
            logger.info(f"Job {job_id} already successfully COMPLETED. Skipping duplicate task.", extra=log_extra)
            return

        # 2. Status Transition
        job_repo.mark_processing(job_id)

        # 3. Logic Execution
        # Result contains: raw_text, structured_data, metadata, plus durations/ai_status
        result = pipeline.run(job_id, job.file_key)

        # 4. Save results (Independent JSON update)
        result_repo.save_result(job_id, result)

        # 5. Finalize with stage-level metadata persistence
        job_repo.mark_completed(
            job_id, 
            final_meta={
                "ocr_duration_ms": result.get("ocr_duration_ms"),
                "ai_duration_ms": result.get("ai_duration_ms"),
                "ai_status": result.get("ai_status"),
                "fallback_used": result.get("fallback_used"),
                "confidence_score": result.get("confidence_score")
            }
        )
        logger.info(f"Job {job_id} finished. Pipeline result enqueued to DB.", extra=log_extra)

    except PipelineError as p_err:
        logger.error(f"Pipeline failure for job {job_id}: {p_err.message}", extra=log_extra)
        job_repo.mark_failed(job_id, error_code=p_err.error_code, error_message=p_err.message)
    except Exception as e:
        logger.error(f"Unexpected system crash for job {job_id}: {str(e)}", extra=log_extra)
        job_repo.mark_failed(job_id, error_code="UNEXPECTED_SYSTEM_ERROR", error_message=str(e))
        # Trigger Celery retry for infrastructure/transient failures
        raise self.retry(exc=e, countdown=60)
    finally:
        job_repo.close()
        result_repo.close()
