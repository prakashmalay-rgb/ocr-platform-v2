# 001: Clean Room Rebuild

**Status**: Accepted
**Date**: 2026-03-29

## Context and Problem Statement
We are building a clean-room V2 OCR SaaS platform completely from scratch.
There must be no reuse of previous OCR project code.

## Rules
- This is a clean-room rebuild. No previous code will be reused, mirrored, or referenced.
- Architecture is fixed:
  - Frontend: Next.js
  - Backend: FastAPI
  - Workers: separate async processing service
  - Database: PostgreSQL
  - Queue: Redis
  - Storage: S3 or S3-compatible object storage
- Only public frameworks and public APIs will be used.
- Do not place business logic in random utility folders.
- No new technologies unless justified first and explicitly approved.

## Service Split
1. **Frontend**: Responsible exclusively for the UI.
2. **Backend**: Responsible for APIs and orchestration.
3. **Workers**: Responsible for extraction, enrichment, and export processing.
