from .ocr.tesseract import TesseractOCRProvider
from .ai.openai import OpenAIProvider

class ProviderFactory:
    @staticmethod
    def get_ocr_provider(provider_name: str = "tesseract"):
        if provider_name == "tesseract":
            return TesseractOCRProvider()
        raise ValueError(f"Unknown OCR provider: {provider_name}")

    @staticmethod
    def get_ai_provider(provider_name: str = "openai"):
        if provider_name == "openai":
            return OpenAIProvider()
        raise ValueError(f"Unknown AI provider: {provider_name}")
