from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # GENERAL
    LOG_LEVEL: str = "INFO"
    DATA_DIR: str = "./temp"  # Default to local temp directory for development

    # API settings
    API_TITLE: str = "Bad Words API"
    API_DESCRIPTION: str = "An API for profanity detection"
    API_VERSION: str = "1.0.0"
    MAX_TEXT_LENGTH: int = Field(default=500, description="Maximum character length for text input")

    # Rate limiting settings
    RATE_LIMIT_DEFAULT: str = "10/minute"

    # AI Settings
    MODEL_NAME: str = Field(
        default="ml6team/distilbert-base-german-cased-toxic-comments",
        description="The AI model to use",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        env_file_path=[".env.local", ".env"],
    )


@lru_cache
def get_settings() -> Settings:
    """
    Create and cache settings instance to avoid reloading from environment
    on each request.

    Returns:
        Settings: Application settings loaded from environment variables
    """
    return Settings()
