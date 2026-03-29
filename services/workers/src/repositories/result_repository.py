from sqlalchemy import text
import json
from ..core.database import SessionLocal

class ResultRepository:
    def __init__(self, db_session=None):
        self.db = db_session or SessionLocal()

    def save_result(self, job_id: str, result_dict: dict):
        """Serializes result to JSON and updates the job record."""
        self.db.execute(
            text("UPDATE jobs SET result_json = :res, updated_at = NOW() WHERE id = :id AND status = 'processing'"),
            {"id": job_id, "res": json.dumps(result_dict)}
        )
        self.db.commit()

    def close(self):
        self.db.close()
