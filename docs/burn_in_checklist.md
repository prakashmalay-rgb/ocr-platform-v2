# Staging Burn-in Checklist (OCR Platform V2)

This document contains the final mission-critical verification steps before production deployment. All 12 items MUST pass in the staging environment (`/V2`).

## 1. Core Lead Generation Flow (Success/Persistence)
- [ ] **Lead Form Success**: Submit form with valid Turnstile token.
    - [ ] Result: UI shows "Thank you!" success message.
    - [ ] DB Check: Verify record exists in `leads` table with all fields.
    - [ ] Notification Check: Receive Resend email notification in business inbox.
    - [ ] Status Check: Record shows `is_notification_sent: True` in DB.

## 2. Security & Abuse Protection
- [ ] **Turnstile (Missing Token)**: Attempt submit without solving widget.
    - [ ] Result: Frontend Zod error blocks submission.
- [ ] **Turnstile (Invalid Token)**: Mock an invalid token in the request.
    - [ ] Result: Backend returns `400 Bad Request` (Robot detection failed).
- [ ] **Rate Limiting**: Submit 6 leads from the same IP within 1 hour.
    - [ ] Result: 6th request returns `429 Too Many Requests`.
    - [ ] Test Verification: Confirm real IP resolution via `X-Forwarded-For`.

## 3. SEO Safety & Protection
- [ ] **Staging Block (/V2)**: Access any page under `/V2`.
    - [ ] Result: Header `X-Robots-Tag: noindex, nofollow, noarchive` is present.
- [ ] **Canonical Strategy**: 
    - [ ] For Parity Pages: Points to `https://www.ocr-extraction.com/[path]`.
    - [ ] For Non-Parity/Staging-only: Canonical tag is omitted entirely.
- [ ] **Dynamic Tool Parity**: Test `image-to-text` and `pdf-to-text`.
    - [ ] Result: Unique H1 and metadata matching the audited manifest.

## 4. Backend Health & Performance
- [ ] **Health Endpoint**: Access `/api/v1/health`.
    - [ ] Result: `{"status": "ok", "version": "v2.0.0"}`.
    - [ ] Arq Worker Connectivity: Enqueue a test OCR job.
    - [ ] Result: Worker picks up and transitions status to `processing` within 2s.
- [ ] **Database Initialization**: Run `python -m app.db.migrate`.
    - [ ] Result: Confirms tables exist or creates missing ones idempotently.

---

## 5. Rollback Triggers (Post-Deploy Alarms)
**ABORT production deployment if any of the following occur during burn-in:**
1.  Frontend `LCP` exceeds 2.5s on tool pages.
2.  Any `Lead Form` submission results in a `500` error (Persistence Failure).
3.  `X-Robots-Tag` is missing from staging pages (Risk of indexing staging).
4.  Database is unreachable from the worker service.

---

## 6. Execution Log
*To be filled during active staging burn-in.*
| Date | Tester | Suite | Result | Issues |
| :--- | :--- | :--- | :--- | :--- |
| | | | | |
