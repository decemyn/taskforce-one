# Task Force One - Dockerfile
# Multi-stage build for optimized production deployment

FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_SYSTEM_PYTHON=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster package installation
RUN pip install uv

# Copy dependency files
COPY pyproject.toml requirements.txt README.md ./

# Install dependencies using uv
RUN uv pip install --system -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config/ ./config/
COPY scripts/ ./scripts/
COPY pytest.ini ./
COPY tests/ ./tests/

# Install the package in editable mode
RUN pip install -e .

# Expose port (default for API services)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command - run the FastAPI server
CMD ["uvicorn", "taskforce_one.api:app", "--host", "0.0.0.0", "--port", "8000"]
