import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from src.config.logging import get_logger

logger = get_logger("api.middleware")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP requests with processing time.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Get request details
        method = request.method
        path = request.url.path
        query_params = str(request.query_params) if request.query_params else ""

        # Start timing
        start_time = time.time()

        # Process the request
        try:
            response = await call_next(request)
            status_code = response.status_code
            success = True
        except Exception as e:
            status_code = 500
            success = False
            # Re-raise the exception after logging
            raise e
        finally:
            # Calculate processing time
            process_time = time.time() - start_time
            process_time_ms = process_time * 1000

            # Log request details
            log_msg = (
                f"{method} {path} {query_params} | "
                f"Status: {status_code} | "
                f"Time: {process_time_ms:.2f}ms"
            )

            if success:
                if status_code >= 500:
                    logger.error(log_msg)
                elif status_code >= 400:
                    logger.warning(log_msg)
                else:
                    logger.info(log_msg)
            else:
                logger.error(log_msg)

        return response


def setup_rate_limiting_middleware(app: FastAPI) -> None:
    """
    Setup rate limiting middleware for the application.

    Args:
        app: The FastAPI application
    """
    app.add_middleware(SlowAPIMiddleware)
    logger.debug("Rate limiting middleware configured")


def add_middleware(app: FastAPI) -> None:
    """
    Add all middlewares to the FastAPI application.

    Args:
        app: The FastAPI application
    """
    # Add rate limiting middleware
    setup_rate_limiting_middleware(app)

    # Add request logging middleware
    app.add_middleware(RequestLoggingMiddleware)

    logger.info("Application middleware configured")
