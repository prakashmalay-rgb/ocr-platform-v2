from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import health, uploads, jobs
from app.core.config import settings
from app.db.init_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Initialize Database Schema
    init_db()
    yield
    # Cleanup logic (if any) would go here

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(health.router, prefix=settings.API_V1_STR, tags=["Health"])
app.include_router(uploads.router, prefix=f"{settings.API_V1_STR}/uploads", tags=["Uploads"])
app.include_router(jobs.router, prefix=f"{settings.API_V1_STR}/jobs", tags=["Jobs"])

@app.get("/")
def root():
    return {"message": "OCR Platform V2 API", "docs": "/docs"}
