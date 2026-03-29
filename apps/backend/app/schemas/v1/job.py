from pydantic import BaseModel
from typing import Optional
from app.models.job import JobStatus

class JobCreateRequest(BaseModel):
    upload_id: int

class JobResponse(BaseModel):
    id: str
    status: JobStatus
    filename: Optional[str]
