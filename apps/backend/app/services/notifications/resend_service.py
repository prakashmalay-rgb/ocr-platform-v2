import resend
from app.core.config import settings
from app.repositories.lead_repository import LeadRepository
import logging

logger = logging.getLogger("backend")

class ResendNotificationService:
    """
    Business-grade lead delivery via Resend API.
    """
    def __init__(self):
        if settings.RESEND_API_KEY:
            resend.api_key = settings.RESEND_API_KEY

    async def send_lead_notification(self, lead_id: str, lead_data: dict):
        """
        Sends HTML notification to the business inbox.
        Atomically updates the lead record with delivery status.
        """
        repo = LeadRepository()
        
        if not settings.RESEND_API_KEY:
            logger.warning(f"RESEND_API_KEY missing. Lead {lead_id} saved but NOT emailed.")
            return

        try:
            # HTML Template for High-Conversion Lead Notification
            html_content = f\"\"\"
            <div style="font-family: sans-serif; padding: 20px; border: 1px solid #eee; border-radius: 8px;">
                <h2 style="color: #2563eb;">New Enterprise Lead Captured</h2>
                <p><strong>Name:</strong> {lead_data.get('full_name')}</p>
                <p><strong>Email:</strong> {lead_data.get('email')}</p>
                <p><strong>Company:</strong> {lead_data.get('company') or 'Not specified'}</p>
                <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                <p><strong>Message:</strong></p>
                <div style="background: #f8fafc; padding: 15px; border-radius: 4px;">
                    {lead_data.get('message')}
                </div>
            </div>
            \"\"\"

            params = {
                "from": "OCR Platform V2 <notifications@ocr-extraction.com>",
                "to": ["support@ocr-extraction.com"],
                "subject": f"🔥 New Lead: {lead_data.get('full_name')} from {lead_data.get('company') or 'Web'}",
                "html": html_content,
            }

            resend.Emails.send(params)
            
            # Update DB Persistence to success
            repo.mark_notified(lead_id, success=True)
            logger.info(f"Notification SENT for Lead {lead_id} via Resend")

        except Exception as e:
            error_msg = f"Resend failure: {str(e)}"
            logger.error(error_msg)
            # Log failure defensively so it is manual-audit ready
            repo.mark_notified(lead_id, success=False, error=error_msg)

resend_service = ResendNotificationService()
