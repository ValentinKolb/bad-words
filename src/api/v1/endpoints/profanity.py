from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field, field_validator
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.config import get_settings
from src.services.profanity import get_profanity_service

router = APIRouter()

# Create limiter for rate limiting
limiter = Limiter(key_func=get_remote_address)


class TextRequest(BaseModel):
    """Request model for text to be checked or censored."""

    text: str = Field(..., description="The text to check for profanity")

    @field_validator("text")
    def validate_text_length(cls, v):
        """Validate that the text is not too long."""
        settings = get_settings()
        max_length = settings.MAX_TEXT_LENGTH

        if len(v) > max_length:
            raise ValueError(f"Text exceeds maximum length of {max_length} characters")
        return v


class CheckResponse(BaseModel):
    """Response model for profanity check."""

    is_profane: bool = Field(..., description="Whether the text contains profanity")
    confidence: float = Field(..., description="Confidence score of the profanity detection (0-1)")
    original_text: str = Field(..., description="The original text that was checked")


# Define error response models
class ErrorResponse(BaseModel):
    """Standard error response model."""

    detail: str = Field(..., description="Detailed error message")
    status_code: int = Field(default=status.HTTP_400_BAD_REQUEST, description="HTTP status code")


@router.post(
    "/check",
    response_model=CheckResponse,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Bad Request - Invalid input (e.g., text too long)",
            "content": {
                "application/json": {
                    "examples": {
                        "Text too long": {
                            "summary": "Text exceeds maximum length",
                            "value": {
                                "detail": "Text exceeds maximum length (see MAX_TEXT_LENGTH setting)",
                                "status_code": 400,
                            },
                        }
                    }
                }
            },
        },
        429: {
            "model": ErrorResponse,
            "description": "Too Many Requests - Rate limit exceeded",
            "content": {
                "application/json": {
                    "example": {"detail": "Rate limit exceeded", "status_code": 429}
                }
            },
        },
    },
    summary="Check Text for Profanity",
    description="Checks if the provided text contains profanity. Maximum text length is defined by MAX_TEXT_LENGTH setting.",
)
async def check_text(
    request: TextRequest,
    profanity_service=Depends(get_profanity_service),
    settings=Depends(get_settings),
):
    """
    Check if the provided text contains profanity.

    Args:
        request: The text request model
        profanity_service: The profanity service singleton
        settings: The application settings

    Returns:
        CheckResponse: The profanity check results

    Raises:
        HTTPException: If the input validation fails
    """

    # Process the request
    result = profanity_service.check_text(
        text=request.text,
    )

    # Add original text to the result
    result["original_text"] = request.text

    return result
