import os
import shutil
from ..exceptions.pipeline import FileLoadError

class FileLoader:
    def __init__(self, base_temp_dir: str = "/tmp/ocr-worker-jobs"):
        self.base_temp_dir = base_temp_dir

    def get_job_dir(self, job_id: str) -> str:
        return os.path.join(self.base_temp_dir, job_id)

    def load_file(self, job_id: str, file_key: str) -> str:
        """
        MOCK loader for Phase 4. 
        In Phase 3/5: Downloads from S3 to job-specific temp dir.
        """
        job_dir = self.get_job_dir(job_id)
        os.makedirs(job_dir, exist_ok=True)
        
        # Simulate local file creation for testing
        local_path = os.path.join(job_dir, "input_file.pdf")
        with open(local_path, "w") as f:
            f.write("mock content")
            
        return local_path

    def cleanup(self, job_id: str):
        """Purges the job-specific temp directory completely."""
        job_dir = self.get_job_dir(job_id)
        if os.path.exists(job_dir):
            shutil.rmtree(job_dir)
