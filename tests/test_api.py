from unittest import mock

import pytest
from fastapi.testclient import TestClient

from src.api.app import create_app
from src.services.profanity import ProfanityService


@pytest.fixture
def mock_profanity_service():
    """Fixture for mocked profanity service."""
    # Use a more strict way of patching that affects the test client
    with mock.patch("src.api.v1.endpoints.profanity.get_profanity_service") as mock_get_service:
        service = mock.MagicMock(spec=ProfanityService)

        # Default behavior: not profane
        service.check_text.return_value = {
            "is_profane": False,
            "confidence": 0.1,
        }

        mock_get_service.return_value = service
        yield service


@pytest.fixture
def client(mock_profanity_service):
    """Fixture for TestClient with mocked dependencies."""
    app = create_app()
    return TestClient(app)


def test_health_endpoint(client):
    """Test the health endpoint."""
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_config_endpoint(client):
    """Test the config endpoint."""
    response = client.get("/api/v1/config")

    assert response.status_code == 200

    data = response.json()
    assert "api_title" in data
    assert "api_description" in data
    assert "version" in data
    assert "rate_limit" in data
    assert "max_text_length" in data
    assert "model_name" in data


def test_check_profanity_clean_text(client, mock_profanity_service):
    """Test check endpoint with clean text."""
    # Configure mock to return clean result with specific confidence
    mock_profanity_service.check_text.return_value = {
        "is_profane": False,
        "confidence": 0.1,
    }

    response = client.post("/api/v1/check", json={"text": "This is a clean text"})

    assert response.status_code == 200

    data = response.json()
    assert "is_profane" in data
    assert "confidence" in data
    assert data["original_text"] == "This is a clean text"


def test_check_profanity_bad_text(client, mock_profanity_service):
    """Test check endpoint with profane text."""
    # Configure mock to return profane result
    mock_profanity_service.check_text.return_value = {
        "is_profane": True,
        "confidence": 0.9,
    }

    response = client.post("/api/v1/check", json={"text": "This is a bad text"})

    assert response.status_code == 200

    data = response.json()
    assert "is_profane" in data
    assert "confidence" in data
    assert data["original_text"] == "This is a bad text"


def test_check_profanity_too_long(client):
    """Test check endpoint with text that exceeds maximum length."""
    # Create a text that's too long
    too_long_text = "x" * 1000

    response = client.post("/api/v1/check", json={"text": too_long_text})

    assert response.status_code == 422  # Validation error (handled by Pydantic)
