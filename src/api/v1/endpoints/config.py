from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from src.config import get_settings

router = APIRouter()


class ConfigResponse(BaseModel):
    """Response model for API configuration."""

    version: str = Field(..., description="API version number")
    api_title: str = Field(..., description="Name of the API")
    api_description: str = Field(..., description="Brief description of the API purpose")
    rate_limit: str = Field(..., description="Default rate limit setting (e.g. 10/minute)")
    max_text_length: int = Field(..., description="Maximum allowed text length in characters")
    model_name: str = Field(..., description="Name of the AI model used for profanity detection")


@router.get(
    "",
    response_model=ConfigResponse,
    summary="Get API Configuration",
    description="Returns the current API configuration including rate limits, text constraints, and model information.",
)
async def get_config(settings=Depends(get_settings)):
    """
    Get the current API configuration.

    Returns:
        ConfigResponse: The API configuration
    """
    return {
        "version": settings.API_VERSION,
        "api_title": settings.API_TITLE,
        "api_description": settings.API_DESCRIPTION,
        "rate_limit": settings.RATE_LIMIT_DEFAULT,
        "max_text_length": settings.MAX_TEXT_LENGTH,
        "model_name": settings.MODEL_NAME,
    }
