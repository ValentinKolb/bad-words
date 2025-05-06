import logging
import sys

from src.config import Settings


def setup_logging(settings: Settings) -> None:
    """
    Setup application logging with a custom format.

    Args:
        settings: Application settings with log level
    """
    log_level = getattr(logging, settings.LOG_LEVEL.upper())

    # Define a custom format with timestamp, level, and module info
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Configure the root logger
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=date_format,
        stream=sys.stdout,
    )

    # Turn down verbosity for some libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.ERROR)

    # Create logger for our application
    logger = logging.getLogger("bad_words")
    logger.setLevel(log_level)

    logger.info(f"Logging initialized at level: {settings.LOG_LEVEL}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the given name.

    Args:
        name: The logger name, typically the module name

    Returns:
        Logger: Configured logger instance
    """
    return logging.getLogger(f"bad_words.{name}")
