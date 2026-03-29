# Production Deployment Runbook - OCR Platform V2

This document outlines the zero-downtime deployment strategy for the V2 stack.

## Architecture Mapping
- **Frontend**: [Vercel](https://vercel.com) (Next.js)
- **API Backend**: [Render Web Service](https://render.com) (FastAPI)
- **Workers**: [Render Background Worker](https://render.com) (Celery)
- **Database**: [Neon Postgres](https://neon.tech) (Serverless, pooled)
- **Queue**: [Upstash Redis](https://upstash.com) or Render Redis
- **Storage**: [Cloudflare R2](https://cloudflare.com) (S3-Compatible)

---

## 1. Infrastructure Provisioning Order

1. **Storage**: Create a Cloudflare R2 bucket (`ocr-v2-prod`). Note the S3-compatible endpoint.
2. **Database**: Create a Neon project. Copy the **Pooled** connection string (`-pooler` suffix).
3. **Queue**: Provision Redis.
4. **API (Render)**:
   - Type: Web Service
   - Root Directory: `apps/backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. **Worker (Render)**:
   - Type: Background Worker
   - Root Directory: `services/workers`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `celery -A src.main.celery_app worker --loglevel=info`

---

## 2. Environment Variables Matrix

### Backend & Worker (Shared Secrets)
| Variable | Value / Source |
| :--- | :--- |
| `DATABASE_URL` | Neon Pooled URL |
| `REDIS_URL` | Redis URL |
| `S3_ENDPOINT_URL` | Cloudflare R2 Endpoint |
| `AWS_ACCESS_KEY_ID` | R2 Access Key |
| `AWS_SECRET_ACCESS_KEY` | R2 Secret Key |
| `S3_BUCKET_NAME` | `ocr-v2-prod` |
| `MAX_FILE_SIZE_BYTES` | `10485760` (10MB) |
| `AI_MAX_CHAR_LIMIT` | `20000` |
| `OPENAI_API_KEY` | production-key |

### Frontend (External only)
| Variable | Value / Source |
| :--- | :--- |
| `NEXT_PUBLIC_API_URL` | Render Web Service URL |

---

## 3. Migration & Launch Sequence

1. **Baseline**: Run first Alembic migration against the Neon DB to establish tables.
2. **Deploy Worker**: Ensure worker is live and listening on Redis before the API.
3. **Deploy API**: Launch Render Web Service.
4. **Deploy Frontend**: Launch Vercel project pointing to the new Render URL.
5. **Verify**: Perform a smoke test (U1, P1, P2 from test matrix).

---

## 4. Operational Maintenance
- **Cleanup**: S3 objects should have a 24h lifecycle policy for `/tmp` or failed uploads.
- **Observability**: Monitor Render logs for `ai_status=failed` to scale AI credits or switch providers.
- **Scaling**: Increase Render worker instances to handle spikes in `PROCESSING` queue depth.
