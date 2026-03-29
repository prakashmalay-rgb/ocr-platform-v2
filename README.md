# OCR Platform V2

A clean-room V2 OCR SaaS Platform built from scratch.

## Monorepo Architecture

- `apps/frontend/`: Next.js frontend application.
- `apps/backend/`: FastAPI core service for orchestration.
- `services/workers/`: Async Python workers for document processing, OCR, and AI abstraction.
- `packages/shared-types/`: Shared type definitions (e.g., TS interfaces, Zod schemas).
- `packages/shared-utils/`: Shared common utility logic.
- `infra/`: Infrastructure definitions, Terraform or Docker related deployments.
- `docs/`: System documentation and decision logs.
- `scripts/`: Useful automation helper scripts.

## Core Stack

- **Frontend**: Next.js
- **Backend**: FastAPI (Python)
- **Workers**: Celery/RQ or equivalent standard async worker service
- **Database**: PostgreSQL
- **Message Broker / Cache**: Redis
- **Storage**: S3-compatible Object Storage

## Local Setup

Refer to `.env.example` to set up environment variables and check out infra/ for docker-compose based scaffolding.
