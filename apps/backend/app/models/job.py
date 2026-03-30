from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean, Float
from enum import Enum as PyEnum
from sqlalchemy.types import Enum
from datetime import datetime
from app.models.base import Base

class JobStatus(str, PyEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)
    filename = Column(String)
    file_key = Column(String)
    
    # Result Data
    result_json = Column(JSON, nullable=True)
    
    # Observability & Hardening
    ocr_duration_ms = Column(Integer, nullable=True)
    ai_duration_ms = Column(Integer, nullable=True)
    ai_status = Column(String, default="pending")  # pending, success, failed, skipped
    fallback_used = Column(Boolean, default=False)
    confidence_score = Column(Float, nullable=True)
    
    # Error Context
    error_code = Column(String, nullable=True)
    error_message = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
