from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from app.db.session import Base

class Upload(Base):
    __tablename__ = "uploads"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_key = Column(String, unique=True, nullable=False)  # S3 Key
    content_type = Column(String)
    file_size_bytes = Column(Integer)
    is_confirmed = Column(Boolean, default=False)  # True once upload to S3 is complete
    created_at = Column(DateTime, default=datetime.utcnow)
