import os
from arq.connections import RedisSettings
from .tasks.extraction_task import process_ocr_document

# Redis Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

async def startup(ctx):
    """Lifecycle hook for worker initialization."""
    pass

async def shutdown(ctx):
    """Lifecycle hook for worker cleanup."""
    pass

class WorkerSettings:
    """Arq Worker Configuration"""
    functions = [process_ocr_document]
    redis_settings = RedisSettings(host=REDIS_HOST, port=REDIS_PORT, database=REDIS_DB)
    on_startup = startup
    on_shutdown = shutdown