from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.job import Job, JobStatus
from app.models.upload import Upload
from app.schemas.v1.job import JobCreateRequest, JobResponse
from app.services.jobs.queue import job_queue_service
import uuid

router = APIRouter()

@router.post("/", response_model=JobResponse)
def create_job(payload: JobCreateRequest, db: Session = Depends(get_db)):
    """Triggers a processing job for a confirmed upload."""
    db_upload = db.query(Upload).filter(Upload.id == payload.upload_id).first()
    if not db_upload:
        raise HTTPException(status_code=404, detail="Upload record not found")
    if not db_upload.is_confirmed:
        raise HTTPException(status_code=400, detail="Upload must be confirmed before processing")

    job_id = str(uuid.uuid4())
    db_job = Job(
        id=job_id,
        user_id=1,  # Placeholder for auth user
        filename=db_upload.filename,
        file_key=db_upload.file_key,
        status=JobStatus.PENDING
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    # Dispatches to queue (Redis)
    job_queue_service.dispatch_processing_job(job_id=job_id, file_key=db_upload.file_key)

    return db_job

@router.get("/{job_id}", response_model=JobResponse)
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    """Fetches current job status and metadata."""
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job
