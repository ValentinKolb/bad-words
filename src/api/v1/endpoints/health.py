from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field

from src.config import get_settings


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(..., description="Current health status of the API (ok if running)")
    version: str = Field(..., description="Current version of the API")


router = APIRouter()


@router.get(
    "",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check if the API is up and running",
)
async def health_check(settings=Depends(get_settings)):
    """
    Health check endpoint to verify the API is running correctly.

    Returns:
        HealthResponse: The health status and API version
    """
    return HealthResponse(
        status="ok",
        version=settings.API_VERSION,
    )
