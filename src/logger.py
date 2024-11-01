import logging
from typing import Optional
import os
from datetime import datetime


class CustomFormatter(logging.Formatter):
    """Custom formatter with colored output and metadata."""

    COLORS = {
        'DEBUG': '\033[0;36m',  # Cyan
        'INFO': '\033[0;32m',  # Green
        'WARNING': '\033[0;33m',  # Yellow
        'ERROR': '\033[0;31m',  # Red
        'CRITICAL': '\033[0;35m',  # Purple
        'RESET': '\033[0m'
    }

    def format(self, record):
        # Add color
        if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
            record.levelname = (
                f"{self.COLORS.get(record.levelname, '')}"
                f"{record.levelname}"
                f"{self.COLORS['RESET']}"
            )

        # Add metadata
        record.timestamp = datetime.now().isoformat()
        if not hasattr(record, 'metadata'):
            record.metadata = {}

        return super().format(record)


def setup_logger(
        name: str,
        log_file: Optional[str] = None,
        level: str = "INFO"
) -> logging.Logger:
    """Configure and return a logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    # Console handler
    console_handler = logging.StreamHandler()
    console_formatter = CustomFormatter(
        '%(timestamp)s - %(name)s - %(levelname)s - %(message)s'
        '%(metadata)s'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler
    if log_file:
        try:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.error(f"Failed to setup file handler: {e}")

    return logger