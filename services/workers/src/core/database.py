from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Worker DB config - Uses backend DB URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@localhost:5432/ocr_db")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    except:
        db.close()
        raise
