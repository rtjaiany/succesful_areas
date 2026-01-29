"""
Logger Configuration

Centralized logging configuration using loguru.
"""

import sys
import os
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def setup_logger():
    """Configure loguru logger with file and console output."""

    # Remove default handler
    logger.remove()

    # Get log level from environment
    log_level = os.getenv("LOG_LEVEL", "INFO")

    # Console handler with colors
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level,
        colorize=True,
    )

    # File handler
    log_file = os.getenv("LOG_FILE", "logs/extraction.log")
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=log_level,
        rotation="10 MB",
        retention="30 days",
        compression="zip",
    )

    logger.info("Logger configured successfully")
