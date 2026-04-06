from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    PROJECT_NAME: str = "OCR Platform V2"
    API_V1_STR: str = "/api/v1"
    
    # DB & Redis
    DATABASE_URL: str = "postgresql+psycopg2://user:password@localhost:5432/ocr_db"
    REDIS_URL: str = "redis://localhost:6379/0"

    @property
    def REDIS_HOST(self) -> str:
        return self.REDIS_URL.split("//")[1].split(":")[0]

    @property
    def REDIS_PORT(self) -> int:
        return int(self.REDIS_URL.split(":")[2].split("/")[0])
    
    # S3 / Object Storage (Aligned with Render Dashboard)
    S3_BUCKET_NAME: str = "ocr-platform-v2"
    S3_REGION: str = "us-east-1"
    
    # Aliases for R2-style naming in Render
    S3_ENDPOINT_URL: Optional[str] = None
    R2_ENDPOINT_URL: Optional[str] = None
    
    AWS_ACCESS_KEY_ID: str = ""
    R2_ACCESS_KEY_ID: Optional[str] = None
    
    AWS_SECRET_ACCESS_KEY: str = ""
    R2_SECRET_ACCESS_KEY: Optional[str] = None

    @property
    def effective_s3_endpoint(self) -> Optional[str]:
        return self.R2_ENDPOINT_URL or self.S3_ENDPOINT_URL

    @property
    def effective_aws_access_key(self) -> str:
        return self.R2_ACCESS_KEY_ID or self.AWS_ACCESS_KEY_ID

    @property
    def effective_aws_secret_key(self) -> str:
        return self.R2_SECRET_ACCESS_KEY or self.AWS_SECRET_ACCESS_KEY

    # Hardening Config
    MAX_FILE_SIZE_BYTES: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_MIME_TYPES: List[str] = ["application/pdf", "image/png", "image/jpeg"]
    AI_MAX_CHAR_LIMIT: int = 20000  # Guard for large raw_text enrichment
    
    # Security
    SECRET_KEY: str = "secret-key-to-be-changed"
    TURNSTILE_SECRET_KEY: Optional[str] = None
    RESEND_API_KEY: Optional[str] = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
