from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from app.schemas.v1.contracts import LeadCreate, LeadResponse
from app.repositories.lead_repository import LeadRepository
from app.services.security.turnstile import turnstile_service
from app.services.notifications.resend_service import resend_service
import time

router = APIRouter()

def get_client_ip(request: Request) -> str:
    """
    Resolve real client IP accounting for Vercel/Render proxy headers.
    Vercel: x-forwarded-for (first entry) or x-real-ip
    """
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"

@router.post(
    "/contact", 
    response_model=LeadResponse,
    responses={
        400: {"description": "Bot check failed"},
        500: {"description": "Persistence error"}
    }
)
async def create_lead(
    lead_in: LeadCreate, 
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    Business-ready lead capture endpoint:
    1. Resolve real client IP (X-Forwarded-For aware)
    2. Enforce bot-check (Turnstile)
    3. Atomically persist to DB LeadRepository
    4. Enqueue background notification
    """
    client_ip = get_client_ip(request)
    
    # 1. Verification (Bot-check)
    is_human = await turnstile_service.verify_token(lead_in.turnstile_token, client_ip)
    if not is_human:
        raise HTTPException(status_code=400, detail="Robot detection failed. Please try again.")

    # 2. Persistence (DB)
    repo = LeadRepository()
    try:
        new_lead = repo.create_lead(lead_in.model_dump(), client_ip)
    except Exception:
        raise HTTPException(status_code=500, detail="Capture system error. Please try again later.")

    # 3. Notification (Async)
    background_tasks.add_task(resend_service.send_lead_notification, str(new_lead.id), lead_in.model_dump())
    
    return LeadResponse(
        id=str(new_lead.id),
        success=True,
        message="Inquiry successfully captured"
    )
