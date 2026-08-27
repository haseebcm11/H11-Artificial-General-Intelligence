# Production Dockerfile for H11-AGI Sovereign Cognitive Operating System
# Domain: h11.network

FROM python:3.12-slim-bullseye AS base

# Install system build dependencies and curl
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    HOST=0.0.0.0 \
    DOMAIN=h11.network

WORKDIR /app

# Copy requirement files and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir fastapi uvicorn[standard] httpx pydantic aiohttp

# Copy repository source code
COPY . .

# Run test verification during build to ensure 100% integrity
RUN python -m unittest discover tests

# Expose server port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Launch the H11-AGI Conversational Reasoning Chat Server
CMD ["python", "-m", "h11_runtime.server"]
