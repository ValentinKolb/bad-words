# Build stage with UV
FROM ghcr.io/astral-sh/uv:bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Configure the Python directory so it is consistent
ENV UV_PYTHON_INSTALL_DIR=/python

# Only use the managed Python version
ENV UV_PYTHON_PREFERENCE=only-managed

# Install Python before the project for caching
RUN uv python install 3.9

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Runtime stage
FROM debian:bookworm-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the Python version
COPY --from=builder --chown=root:root /python /python
ENV PATH="/python/bin:$PATH"

# Create app user
RUN groupadd -r app && useradd -r -g app app

# Create app directory structure
RUN mkdir -p /app/data && chown -R app:app /app

# Copy the application from the builder
COPY --from=builder --chown=app:app /app /app

# Set working directory
WORKDIR /app

# Configure environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DATA_DIR=/app/data

# Set user
USER app

# Expose port
EXPOSE 8000

# Use entrypoint and cmd for better container flexibility
ENTRYPOINT ["python"]
CMD ["main.py"]

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8000/api/v1/health || exit 1