from sqlalchemy import create_engine, inspect
from app.db.base import Base
from app.core.config import settings
import logging

# Ensure ALL models are imported so Base.metadata is fully populated
from app.models.job import Job
from app.models.lead import Lead

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("db_init")

def run_migrations():
    """
    Idempotent database initialization.
    Safe for repeated execution on Vercel/Render post-deploy.
    """
    engine = create_engine(settings.DATABASE_URL)
    inspector = inspect(engine)
    
    # 1. Verification: Check if business critical tables exist
    target_tables = ["jobs", "leads"]
    existing_tables = inspector.get_table_names()
    
    missing = [t for t in target_tables if t not in existing_tables]
    
    if not missing:
        logger.info("All database tables verified. Skipping creation.")
        return

    # 2. Deployment-Safe Creation
    logger.info(f"Missing tables: {missing}. Executing Base.metadata.create_all...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database schema initialized successfully.")
    except Exception as e:
        logger.critical(f"FATAL: Database initialization failed: {str(e)}")
        raise e

if __name__ == "__main__":
    run_migrations()
