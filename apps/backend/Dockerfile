FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (e.g., libmagic for some libraries if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual app folder
COPY app/ ./app/

# Use $PORT environment variable for Render compatibility (defaulting to 10000)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
