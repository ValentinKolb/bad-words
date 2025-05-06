from fastapi import FastAPI
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from src.api.middleware import add_middleware
from src.api.v1.router import v1_router
from src.config import get_settings
from src.config.logging import get_logger, setup_logging

logger = get_logger("api.app")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application
    """
    settings = get_settings()

    # Setup logging based on settings
    setup_logging(settings)
    logger.info(f"Starting {settings.API_TITLE} v{settings.API_VERSION}")

    # Create limiter for rate limiting
    # This can be configured to use Redis later by changing the storage_uri
    # Example with Redis: Limiter(key_func=get_remote_address, storage_uri="redis://localhost:6379")
    limiter = Limiter(key_func=get_remote_address)

    # Create FastAPI app with metadata
    app = FastAPI(
        title=settings.API_TITLE,
        description=settings.API_DESCRIPTION,
        version=settings.API_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Configure exception handlers
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Add all middleware
    add_middleware(app)

    # Include routers
    app.include_router(v1_router, prefix="/api/v1")
    logger.info("API routes configured")

    return app


async def _rate_limit_exceeded_handler(request, exc):
    """Handle rate limit exceeded exceptions."""
    from fastapi import status
    from fastapi.responses import JSONResponse

    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "detail": "Rate limit exceeded",
            "status_code": 429,
        },
    )
