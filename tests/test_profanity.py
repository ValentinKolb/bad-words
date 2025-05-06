from unittest import mock

import pytest

from src.config import Settings
from src.services.profanity import ProfanityService


class MockModel:
    """Mock for the Hugging Face model."""

    def __init__(self):
        self.eval_called = False

    def __call__(self, **kwargs):
        """Mock for the model call."""

        class Outputs:
            def __init__(self):
                import torch

                self.logits = torch.tensor([[0.2, 0.8]])

        return Outputs()

    def eval(self):
        """Mock for the model.eval call."""
        self.eval_called = True
        return self

    def save_pretrained(self, path):
        """Mock for the model.save_pretrained call."""
        pass


class MockTokenizer:
    """Mock for the Hugging Face tokenizer."""

    def __call__(self, text, **kwargs):
        """Mock for the tokenizer call."""
        return {"input_ids": [1, 2, 3], "attention_mask": [1, 1, 1]}

    def save_pretrained(self, path):
        """Mock for the tokenizer.save_pretrained call."""
        pass


@pytest.fixture
def mock_settings():
    """Fixture for settings."""
    settings = Settings()
    settings.DATA_DIR = "/tmp/data"
    settings.MODEL_NAME = "test-model"
    return settings


@pytest.fixture
def mock_service(mock_settings):
    """Fixture for profanity service with mocked model."""
    with (
        mock.patch("src.services.profanity.AutoModelForSequenceClassification") as mock_model_cls,
        mock.patch("src.services.profanity.AutoTokenizer") as mock_tokenizer_cls,
        mock.patch("src.services.profanity.Path") as mock_path,
        mock.patch("torch.no_grad"),
    ):
        # Setup model and tokenizer mocks
        model = MockModel()
        tokenizer = MockTokenizer()

        mock_model_cls.from_pretrained.return_value = model
        mock_tokenizer_cls.from_pretrained.return_value = tokenizer

        # Setup path mocks
        mock_path.return_value.exists.return_value = False
        mock_path.return_value.__truediv__.return_value = mock_path.return_value
        mock_path.return_value.mkdir.return_value = None

        service = ProfanityService(mock_settings)

        yield service


def test_profanity_service_init(mock_service):
    """Test that the profanity service initializes correctly."""
    assert mock_service.threshold == 0.5
    assert mock_service.model.eval_called is True


def test_check_text_basic(mock_service):
    """Test that check_text returns appropriate structure."""
    # Just test basic functionality without exact values
    result = mock_service.check_text("This is a text")

    assert "is_profane" in result
    assert isinstance(result["is_profane"], bool)
    assert "confidence" in result
    assert isinstance(result["confidence"], float)


def test_threshold_property(mock_service):
    """Test that the threshold property can be modified."""
    # Get default threshold
    default_threshold = mock_service.threshold

    # Set a different threshold
    mock_service.threshold = 0.9

    # Check that it was set correctly
    assert mock_service.threshold == 0.9
    assert mock_service.threshold != default_threshold
