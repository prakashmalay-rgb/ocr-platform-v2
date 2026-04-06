import logging
from app.repositories.lead_repository import LeadRepository
import asyncio

logger = logging.getLogger("backend")

async def send_lead_notification(lead_id: str, _email_data: dict):
    """
    Downstream notification task.
    In production: Replace with SendGrid/AWS SES call.
    Includes persistent result auditing for Phase 2 visibility.
    """
    repo = LeadRepository()
    
    try:
        # 1. Audit Start
        logger.info(f"Triggering email notification for Lead {lead_id}")
        
        # 2. Simulate real network call reliability
        await asyncio.sleep(1) 
        
        # 3. Mark success atomically
        repo.mark_notified(lead_id, success=True)
        logger.info(f"Notification success for Lead {lead_id}")
        
    except Exception as e:
        logger.error(f"Downstream delivery CRASHED for Lead {lead_id}: {str(e)}")
        repo.mark_notified(lead_id, success=False, error=str(e))
