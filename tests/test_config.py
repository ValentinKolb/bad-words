import os
import tempfile
from unittest import mock

from src.config.settings import Settings, get_settings


def test_default_settings():
    """Test that default settings are loaded correctly."""
    settings = Settings()

    assert settings.LOG_LEVEL == "INFO"
    assert settings.API_TITLE == "Bad Words API"
    assert settings.API_DESCRIPTION == "An API for profanity detection"
    assert settings.API_VERSION == "1.0.0"
    assert settings.MAX_TEXT_LENGTH == 500
    assert settings.RATE_LIMIT_DEFAULT == "10/minute"
    assert settings.MODEL_NAME == "ml6team/distilbert-base-german-cased-toxic-comments"


def test_settings_from_env_vars():
    """Test that settings can be overridden by environment variables."""
    with mock.patch.dict(
        os.environ,
        {
            "LOG_LEVEL": "DEBUG",
            "API_TITLE": "Custom API",
            "API_DESCRIPTION": "Custom description",
            "API_VERSION": "2.0.0",
            "MAX_TEXT_LENGTH": "1000",
            "RATE_LIMIT_DEFAULT": "20/minute",
            "MODEL_NAME": "custom-model",
        },
    ):
        settings = Settings()

        assert settings.LOG_LEVEL == "DEBUG"
        assert settings.API_TITLE == "Custom API"
        assert settings.API_DESCRIPTION == "Custom description"
        assert settings.API_VERSION == "2.0.0"
        assert settings.MAX_TEXT_LENGTH == 1000
        assert settings.RATE_LIMIT_DEFAULT == "20/minute"
        assert settings.MODEL_NAME == "custom-model"


def test_settings_singleton():
    """Test that get_settings returns a singleton instance."""
    settings1 = get_settings()
    settings2 = get_settings()

    assert settings1 is settings2


def test_data_dir_settings():
    """Test that DATA_DIR is correctly set from environment."""
    with tempfile.TemporaryDirectory() as temp_dir:
        test_path = os.path.join(temp_dir, "test_data")

        with mock.patch.dict(os.environ, {"DATA_DIR": test_path}):
            settings = Settings()

            assert test_path == settings.DATA_DIR
