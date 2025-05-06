import time
from functools import lru_cache
from pathlib import Path
from typing import Any

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from src.config import Settings, get_settings
from src.config.logging import get_logger

logger = get_logger("services.profanity")


class ProfanityService:
    """
    Service for detecting profanity in text.
    """

    def __init__(self, s: Settings):
        """
        Initialize the profanity service with persistent model storage.

        Models are loaded from disk if available, otherwise downloaded and saved
        for future use.
        """
        logger.info(f"Initializing ProfanityService with model: {s.MODEL_NAME}")
        start_time = time.time()

        model_dir = Path(s.DATA_DIR) / "models" / s.MODEL_NAME

        # Create model directory if it doesn't exist
        model_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Using model directory: {model_dir}")

        model_path = model_dir / "model"
        tokenizer_path = model_dir / "tokenizer"

        # Check if the model and tokenizer have been saved locally
        if model_path.exists() and tokenizer_path.exists():
            # Load from local storage
            logger.info(f"Loading model from cache: {model_path}")
            self.model = AutoModelForSequenceClassification.from_pretrained(str(model_path))
            self.tokenizer = AutoTokenizer.from_pretrained(str(tokenizer_path))
            logger.info(f"Model loaded from cache in {time.time() - start_time:.2f}s")
        else:
            # Download and save for future use
            logger.info(f"Downloading model: {s.MODEL_NAME}")
            self.model = AutoModelForSequenceClassification.from_pretrained(s.MODEL_NAME)
            self.tokenizer = AutoTokenizer.from_pretrained(s.MODEL_NAME)

            # Save model and tokenizer
            logger.info(f"Saving model to: {model_path}")
            self.model.save_pretrained(str(model_path))
            self.tokenizer.save_pretrained(str(tokenizer_path))
            logger.info(f"Model downloaded and saved in {time.time() - start_time:.2f}s")

        # Configurable threshold, could be moved to settings if needed
        self.threshold = 0.5

        # Set model to evaluation mode for inference
        self.model.eval()

        logger.info("ProfanityService initialization complete")

    def check_text(self, text: str) -> dict[str, Any]:
        """
        Check if text contains profanity.

        Args:
            text: The text to check

        Returns:
            Dict: Results containing whether is_profane (bool) and confidence score (0-1)
        """
        logger.debug(f"Processing text: {text[:30]}...")

        # Tokenize the input text
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)

        with torch.no_grad():
            # Get model outputs (no need for attention in production)
            outputs = self.model(**inputs)

            # Get prediction score
            prediction = torch.softmax(outputs.logits, dim=1)[0][1].item()

        is_profane = prediction > self.threshold
        logger.debug(f"Profanity check result: {is_profane} (confidence: {prediction:.4f})")

        return {
            "is_profane": is_profane,
            "confidence": prediction,
        }


@lru_cache
def get_profanity_service() -> ProfanityService:
    """
    Create and cache a singleton instance of the ProfanityService.

    Returns:
        ProfanityService: A singleton instance of the profanity detection service
    """
    return ProfanityService(get_settings())
