import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200

def test_lead_capture_validation():
    # Empty payload
    response = client.post("/api/v1/leads/contact", json={})
    assert response.status_code == 422
    # Note: Backend Pydantic schema uses snake_case, so it expects full_name/turnstile_token
    # But frontend is likely camelCase (from common TS pattern).
    # Let's ensure our backend handles camelCase or we fix the frontend mapping.
    
def test_lead_capture_success():
    payload = {
        "full_name": "Audit User",
        "email": "audit@example.com",
        "message": "This is a valid test inquiry for OCR migration.",
        "turnstile_token": "test-token"
    }
    response = client.post("/api/v1/leads/contact", json=payload)
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_lead_capture_rate_limit():
    payload = {
        "full_name": "Rapid User",
        "email": "rapid@example.com",
        "message": "Testing 429 rate limit behavior.",
        "turnstile_token": "token"
    }
    # Send 6 requests (Limit is 5 per hour)
    for _ in range(5):
        client.post("/api/v1/leads/contact", json=payload)
    
    response = client.post("/api/v1/leads/contact", json=payload)
    assert response.status_code == 429
    assert "Too many inquiries" in response.json()["detail"]
