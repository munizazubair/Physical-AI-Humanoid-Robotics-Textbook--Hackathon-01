"""
Logging Configuration

Configures centralized logging for the RAG chatbot backend with
rotating file handlers and console output.
"""

import logging
import logging.handlers
import os
from pathlib import Path


def setup_logging(log_level: str = "INFO"):
    """
    Configure application logging with rotating file handler.

    Args:
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # Clear existing handlers
    root_logger.handlers.clear()

    # Create formatter with session context
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler (stdout)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Rotating file handler for general logs
    file_handler = logging.handlers.RotatingFileHandler(
        filename=log_dir / "rag_chatbot.log",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=7,  # Keep 7 days of logs
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Rotating file handler for errors only
    error_handler = logging.handlers.RotatingFileHandler(
        filename=log_dir / "errors.log",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=30,  # Keep 30 days of error logs
        encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    root_logger.addHandler(error_handler)

    # Suppress noisy third-party loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    logging.info(f"Logging configured with level: {log_level}")
    logging.info(f"Log directory: {log_dir.absolute()}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a module.

    Args:
        name (str): Logger name (typically __name__)

    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)
