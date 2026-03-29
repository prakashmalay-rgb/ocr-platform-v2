# Architecture Overview (V2 OCR SaaS Platform)

The platform architecture is structured around strict separation of concerns, providing clear boundaries for scale and security.

- **Frontend Application (Next.js)**: Handles user interaction, displaying the dashboard, tracking jobs, uploading images or PDFs, and rendering structured results.
- **Backend API (FastAPI)**: Serves as the primary orchestration layer. Connects to the database and queue, manages user uploads (presigned URLs), and queues processing jobs.
- **Workers (Async Services)**: Poll Redis for pending jobs. Handle heavy OCR processing, enrichment, AI summary, and document exports.
- **Database (PostgreSQL)**: Stores user accounts, billing, job history, and extracted structured JSON outputs.
- **Queue (Redis)**: Facilitates job distribution to the OCR pipelines.
- **Storage (S3)**: Stores uploaded files and completed export artifacts.
