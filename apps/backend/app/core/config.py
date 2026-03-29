from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    PROJECT_NAME: str = "OCR Platform V2"
    API_V1_STR: str = "/api/v1"
    
    # DB & Redis
    DATABASE_URL: str = "postgresql+psycopg2://user:password@localhost:5432/ocr_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # S3 / Object Storage
    S3_BUCKET_NAME: str = "ocr-platform-v2"
    S3_REGION: str = "us-east-1"
    S3_ENDPOINT_URL: Optional[str] = None
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""

    # Hardening Config
    MAX_FILE_SIZE_BYTES: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_MIME_TYPES: List[str] = ["application/pdf", "image/png", "image/jpeg"]
    AI_MAX_CHAR_LIMIT: int = 20000  # Guard for large raw_text enrichment
    
    # Security
    SECRET_KEY: str = "secret-key-to-be-changed"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
