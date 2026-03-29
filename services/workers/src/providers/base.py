from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseOCRProvider(ABC):
    @abstractmethod
    def extract_text(self, file_path: str, job_id: str) -> Dict[str, Any]:
        """Returns raw text and basic metadata (pages, confidence)."""
        pass

class BaseAIProvider(ABC):
    @abstractmethod
    def structure_content(self, raw_text: str, job_id: str) -> Dict[str, Any]:
        """Returns structured JSON, summary, and AI insights."""
        pass
