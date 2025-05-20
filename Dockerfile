# Build stage with UV using the official Python+UV image
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

# Configure UV environment variables
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
# Use system Python to avoid compatibility issues between stages
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Copy application code
COPY . /app

# Install project dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Runtime stage - uses matching Python version from official image
FROM python:3.13-slim-bookworm

# Install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the application from the builder
COPY --from=builder --chown=app:app /app /app

# Set working directory
WORKDIR /app

# Add .venv binaries to PATH
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DATA_DIR=/app/data

# Expose port
EXPOSE 8000

# Use Python from PATH to run main.py
ENTRYPOINT ["python"]
CMD ["main.py"]

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8000/api/v1/health || exit 1