from sqlalchemy import Column, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.base import Base
import uuid

class Lead(Base):
    """
    Lead model for capturing business inquiries.
    """
    __tablename__ = "leads"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, index=True)
    company = Column(String(100), nullable=True)
    message = Column(Text, nullable=False)
    
    # Metadata for fraud detection & operational auditing
    client_ip = Column(String(45), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    source_env = Column(String(20), default="production", nullable=False)
    is_synced_to_crm = Column(Boolean, default=False)
    is_notification_sent = Column(Boolean, default=False)
    last_sync_error = Column(Text, nullable=True)
