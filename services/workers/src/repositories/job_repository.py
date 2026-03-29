from sqlalchemy import text
from ..core.database import SessionLocal
import json

class JobRepository:
    def __init__(self, db_session=None):
        self.db = db_session or SessionLocal()

    def get_job_status(self, job_id: str):
        result = self.db.execute(
            text("SELECT status, file_key FROM jobs WHERE id = :id"),
            {"id": job_id}
        ).fetchone()
        return result

    def mark_processing(self, job_id: str):
        self.db.execute(
            text("UPDATE jobs SET status = 'processing', updated_at = NOW() WHERE id = :id"),
            {"id": job_id}
        )
        self.db.commit()

    def mark_completed(self, job_id: str, final_meta: dict):
        """Atomically updates final stage-level metadata (durations, fallback) during completion."""
        self.db.execute(
            text("""
                UPDATE jobs 
                SET status = 'completed', 
                    ocr_duration_ms = :ocr_d, 
                    ai_duration_ms = :ai_d,
                    ai_status = :ai_s,
                    fallback_used = :fb,
                    confidence_score = :conf,
                    updated_at = NOW() 
                WHERE id = :id
            """),
            {
                "id": job_id, 
                "ocr_d": final_meta.get("ocr_duration_ms"),
                "ai_d": final_meta.get("ai_duration_ms"),
                "ai_s": final_meta.get("ai_status", "skipped"),
                "fb": final_meta.get("fallback_used", False),
                "conf": final_meta.get("confidence_score")
            }
        )
        self.db.commit()

    def mark_failed(self, job_id: str, error_code: str, error_message: str):
        self.db.execute(
            text("""
                UPDATE jobs 
                SET status = 'failed', error_code = :code, error_message = :msg, updated_at = NOW() 
                WHERE id = :id
            """),
            {"id": job_id, "code": error_code, "msg": error_message}
        )
        self.db.commit()

    def close(self):
        self.db.close()
