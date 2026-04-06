from sqlalchemy.orm import Session
from app.models.lead import Lead
from app.db.init_db import SessionLocal
import logging

logger = logging.getLogger("backend")

class LeadRepository:
    """
    Persistence layer for reliable lead capture & operational tracking.
    """
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()

    def create_lead(self, data: dict, client_ip: str) -> Lead:
        """Atomically persist a lead from the contact form."""
        try:
            new_lead = Lead(
                full_name=data["full_name"],
                email=data["email"],
                company=data.get("company"),
                message=data["message"],
                client_ip=client_ip,
                source_env=data.get("source_env", "production")
            )
            self.db.add(new_lead)
            self.db.commit()
            self.db.refresh(new_lead)
            return new_lead
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to persist lead logic: {str(e)}")
            raise e
        finally:
            self.db.close()

    def mark_notified(self, lead_id: str, success: bool = True, error: str = None):
        """Audit log for downstream notification status."""
        try:
            lead = self.db.query(Lead).filter(Lead.id == lead_id).first()
            if lead:
                lead.is_notification_sent = success
                if error:
                    lead.last_sync_error = error
                self.db.commit()
        finally:
            self.db.close()
