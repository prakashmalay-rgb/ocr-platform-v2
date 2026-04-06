from ..main import app as celery_app
from ..repositories.job_repository import JobRepository
from ..repositories.result_repository import ResultRepository
from ..pipelines.extraction_pipeline import ExtractionPipeline
from ..exceptions.pipeline import PipelineError
import logging
import sys

# Core worker logger using structured JSON formatter
logger = logging.getLogger("worker")

import logging
from ..repositories.job_repository import JobRepository
from ..repositories.result_repository import ResultRepository
from ..pipelines.extraction_pipeline import ExtractionPipeline
from ..exceptions.pipeline import PipelineError

logger = logging.getLogger("worker")

async def process_ocr_document(ctx, job_id: str, file_key: str):
    """
    Arq Async Orchestrator:
    1. Fetch metadata & state safety
    2. Status Transition to 'processing'
    3. Pipeline execution (Tesseract + LLM enrichment)
    4. Independent result persistence.
    """
    job_repo = JobRepository()
    result_repo = ResultRepository()
    pipeline = ExtractionPipeline()
    log_extra = {"job_id": job_id}

    try:
        # 1. State Safety Check
        job = job_repo.get_job_status(job_id)
        if not job:
            logger.error(f"Job {job_id} not found in DB.", extra=log_extra)
            return

        if job.status == "completed":
            logger.info(f"Job {job_id} already COMPLETED. Skipping duplicate.", extra=log_extra)
            return

        # 2. Transition
        job_repo.mark_processing(job_id)

        # 3. Pipeline Execution
        # result contains: raw_text, structured_data, confidence_score
        result = await pipeline.run_async(job_id, file_key)

        # 4. Persistence
        result_repo.save_result(job_id, result)

        # 5. Finalize
        job_repo.mark_completed(
            job_id,
            final_meta={
                "ocr_engine": result.get("ocr_engine", "tesseract_v4"),
                "confidence_score": result.get("confidence_score"),
                "pages": result.get("pages", 1)
            }
        )
        logger.info(f"Job {job_id} successfully processed.", extra=log_extra)

    except PipelineError as p_err:
        logger.error(f"Pipeline error for job {job_id}: {p_err.message}", extra=log_extra)
        job_repo.mark_failed(job_id, error_code=p_err.error_code, error_message=p_err.message)
    except Exception as e:
        logger.error(f"System crash for job {job_id}: {str(e)}", extra=log_extra)
        job_repo.mark_failed(job_id, error_code="CRITICAL_SYSTEM_ERROR", error_message=str(e))
    finally:
        job_repo.close()
        result_repo.close()
