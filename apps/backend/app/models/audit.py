from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from datetime import datetime
from app.db.session import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    job_id = Column(String, nullable=True)
    action = Column(String, nullable=False)  # e.g., "job_created", "file_uploaded"
    actor_type = Column(String, default="user")  # user, system, worker
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
