class PipelineError(Exception):
    """Base exception for all worker pipeline failures."""
    def __init__(self, message: str, error_code: str = "PIPELINE_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class FileLoadError(PipelineError):
    """Raised when S3 ingestion fails."""
    def __init__(self, message: str):
        super().__init__(message, error_code="FILE_LOAD_ERROR")

class ExtractionError(PipelineError):
    """Raised when OCR processing fails."""
    def __init__(self, message: str):
        super().__init__(message, error_code="EXTRACTION_ERROR")

class StorageError(PipelineError):
    """Raised when result persistence fails."""
    def __init__(self, message: str):
        super().__init__(message, error_code="STORAGE_ERROR")
