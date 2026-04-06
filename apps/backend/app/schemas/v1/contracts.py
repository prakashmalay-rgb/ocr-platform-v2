from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class JobMetadata(BaseModel):
    pages: int
    ocr_engine: str
    timestamp: datetime
    processing_time_ms: int

class UnifiedResult(BaseModel):
    version: str = "v2"
    job_id: str
    metadata: JobMetadata
    raw_text: str
    structured_data: Dict[str, Any]
    confidence_score: float

class JobResponse(BaseModel):
    job_id: str
    status: JobStatus
    created_at: datetime
    processed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    result: Optional[UnifiedResult] = None

class LeadCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    company: Optional[str] = Field(None, max_length=100)
    message: str = Field(..., min_length=10, max_length=2000)
    turnstile_token: str  # Token for abuse protection
    source_env: str = "production"

class LeadResponse(BaseModel):
    id: str
    success: bool = True
    message: str = "Lead captured successfully"
