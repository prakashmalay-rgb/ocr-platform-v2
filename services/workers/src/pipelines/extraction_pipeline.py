import time
from datetime import datetime
from ..loaders.file_loader import FileLoader
from ..providers.factory import ProviderFactory
from ..pipelines.preprocessing import PreprocessingStage
from ..exceptions.pipeline import ExtractionError, PipelineError
from ..core.logging import logger

# Config constants (simulated)
MAX_AI_CHARS = 20000 

class ExtractionPipeline:
    def __init__(self):
        self.loader = FileLoader()
        self.preprocessing = PreprocessingStage()
        self.ocr_provider = ProviderFactory.get_ocr_provider("tesseract")
        self.ai_provider = ProviderFactory.get_ai_provider("openai")

    def run(self, job_id: str, file_key: str) -> dict:
        log_extra = {"job_id": job_id}
        start_time = time.time()
        
        result = {
            "version": "1.0",
            "job_id": job_id,
            "metadata": {"timestamp": datetime.utcnow().isoformat() + "Z"},
            "ai_status": "pending",
            "fallback_used": False
        }

        try:
            # 1. Load & Preprocess
            local_path = self.loader.load_file(job_id, file_key)
            prepped_path = self.preprocessing.process(local_path)
            
            # 2. OCR Stage (MANDATORY)
            ocr_start = time.time()
            ocr_res = self.ocr_provider.extract_text(prepped_path, job_id)
            result["ocr_duration_ms"] = int((time.time() - ocr_start) * 1000)
            result["raw_text"] = ocr_res["raw_text"]
            result["metadata"]["ocr_engine"] = ocr_res["metadata"]["ocr_engine"]
            result["confidence_score"] = ocr_res["metadata"]["confidence_score"]
            result["metadata"]["pages"] = ocr_res["metadata"]["pages"]

            # 3. AI Stage (OPTIONAL ENRICHMENT)
            # Hardening: Chunking guard
            text_to_ai = result["raw_text"]
            if len(text_to_ai) > MAX_AI_CHARS:
                logger.warning(f"Text length {len(text_to_ai)} exceeds limit. Truncating for AI.", extra=log_extra)
                text_to_ai = text_to_ai[:MAX_AI_CHARS]
                result["fallback_used"] = True

            ai_start = time.time()
            try:
                ai_res = self.ai_provider.structure_content(text_to_ai, job_id)
                result["structured_data"] = ai_res["structured_data"]
                result["metadata"]["ai_engine"] = ai_res["metadata"]["ai_engine"]
                result["ai_status"] = "success"
                result["ai_duration_ms"] = int((time.time() - ai_start) * 1000)
            except Exception as ai_err:
                # Reliability: FALLBACK on AI failure. Job remains COMPLETED but without structuring.
                logger.error(f"AI Enrichment failed for {job_id}: {str(ai_err)}", extra=log_extra)
                result["ai_status"] = "failed"
                result["fallback_used"] = True
                result["structured_data"] = {}
                result["metadata"]["ai_engine"] = "none (fallback)"

            result["processing_time_ms"] = int((time.time() - start_time) * 1000)
            return result
        
        except PipelineError as p_err:
            raise p_err
        except Exception as e:
            raise ExtractionError(f"Critical execution error: {str(e)}")
        finally:
            self.loader.cleanup(job_id)
