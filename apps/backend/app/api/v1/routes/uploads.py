from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.upload import Upload
from app.schemas.v1.upload import UploadRequest, UploadResponse, UploadConfirmRequest
from app.services.storage.s3 import storage_service
from app.core.config import settings
import uuid

router = APIRouter()

@router.post("/presigned-url", response_model=UploadResponse)
def get_upload_url(payload: UploadRequest, db: Session = Depends(get_db)):
    """Validates requested MIME type before generating presigned URL."""
    if payload.content_type not in settings.ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_key = f"uploads/{uuid.uuid4()}-{payload.filename}"
    
    db_upload = Upload(
        user_id=1,
        filename=payload.filename,
        file_key=file_key,
        content_type=payload.content_type
    )
    db.add(db_upload)
    db.commit()
    db.refresh(db_upload)

    presigned_url = storage_service.generate_presigned_upload_url(
        bucket=settings.S3_BUCKET_NAME,
        key=file_key
    )

    return {
        "upload_id": db_upload.id,
        "file_key": file_key,
        "presigned_url": presigned_url
    }

@router.post("/confirm")
def confirm_upload(payload: UploadConfirmRequest, db: Session = Depends(get_db)):
    """Hardened confirmation: verify ACTUAL object state in S3 via HEAD."""
    db_upload = db.query(Upload).filter(Upload.id == payload.upload_id).first()
    if not db_upload:
        raise HTTPException(status_code=404, detail="Upload record not found")
    
    # Integrity check: perform HEAD request to S3
    metadata = storage_service.get_object_metadata(settings.S3_BUCKET_NAME, db_upload.file_key)
    
    if not metadata:
        raise HTTPException(status_code=400, detail="File not found in storage. Confirmation failed.")

    # Hardening: Validate size and type from ACTUAL S3 metadata
    if metadata["size_bytes"] > settings.MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File too large. Limits exceeded.")
    
    # Ensure client didn't spoof MIME type vs. actual upload headers
    if metadata["content_type"] not in settings.ALLOWED_MIME_TYPES:
         raise HTTPException(status_code=400, detail="MIME type mismatch/illegal.")

    db_upload.is_confirmed = payload.is_success
    db_upload.file_size_bytes = metadata["size_bytes"]
    db.commit()
    return {"message": "Upload verified and confirmed", "size": metadata["size_bytes"]}
