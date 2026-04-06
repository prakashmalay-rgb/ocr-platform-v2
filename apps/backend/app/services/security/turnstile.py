import httpx
from app.core.config import settings
import logging

logger = logging.getLogger("backend")

class TurnstileService:
    """
    Business-ready verification for Cloudflare Turnstile tokens.
    """
    VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"

    async def verify_token(self, token: str, client_ip: str) -> bool:
        """
        Server-side validation of the bot-check token.
        Fails CLOSED if the request errors to ensure maximum security.
        """
        # Feature flag for testing or dev
        if settings.SECRET_KEY == "debug_site_verification":
            return True

        if not settings.TURNSTILE_SECRET_KEY:
            logger.warning("Turnstile Secret Key is missing. Skipping verification (risky).")
            return True

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    self.VERIFY_URL,
                    data={
                        "secret": settings.TURNSTILE_SECRET_KEY,
                        "response": token,
                        "remoteip": client_ip
                    }
                )
                data = response.json()
                
                if not data.get("success"):
                    logger.warning(f"Turnstile verification FAILED for IP {client_ip}: {data.get('error-codes')}")
                    return False
                
                return True
        except Exception as e:
            logger.error(f"Turnstile verification CRASHED: {str(e)}")
            # Fail closed to prevent malicious bot waves during system downtime
            return False

turnstile_service = TurnstileService()
