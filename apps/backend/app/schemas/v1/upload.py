from pydantic import BaseModel
from typing import Optional

class UploadRequest(BaseModel):
    filename: str
    content_type: str

class UploadResponse(BaseModel):
    upload_id: int
    file_key: str
    presigned_url: str

class UploadConfirmRequest(BaseModel):
    upload_id: int
    is_success: bool
