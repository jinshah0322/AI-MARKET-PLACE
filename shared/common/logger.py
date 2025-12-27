"""
Centralized logging configuration.

Features:
- JSON formatted logs (easy to parse)
- Request ID tracking (trace requests across services)
- Log levels (DEBUG, INFO, WARNING, ERROR)
- Integration with monitoring tools
"""

import logging
import sys
from pythonjsonlogger import json
from typing import Optional
import os


def setup_logger(
        name: str,
        level: str = "INFO",
        log_file: Optional[str] = None
) -> logging.Logger:
    """
    Setup a logger with JSON formatting.

    Args:
        name: Logger name (usually service name)
        level: Log level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional file path to write logs

    Returns:
        Configured logger instance

    Example:
        logger = setup_logger("auth-service")
        logger.info("User registered", extra={"user_id": "123"})
    """
    logger = logging.getLogger(name)

    # Set log level
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)

    # Don't propagate to root logger (avoid duplicate logs)
    logger.propagate = False

    # Remove existing handlers
    logger.handlers = []

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    # JSON formatter
    formatter = json.JsonFormatter(
        fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
        rename_fields={
            "asctime": "timestamp",
            "levelname": "level",
            "name": "service"
        }
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Create a default logger for shared utilities
logger = setup_logger("shared")


# Example usage function
def log_request(
        logger: logging.Logger,
        method: str,
        path: str,
        status_code: int,
        duration_ms: float,
        user_id: Optional[str] = None
) -> None:
    """
    Log an HTTP request with structured data.

    Args:
        logger: Logger instance
        method: HTTP method (GET, POST, etc.)
        path: Request path
        status_code: HTTP status code
        duration_ms: Request duration in milliseconds
        user_id: Optional user ID
    """
    logger.info(
        "HTTP request completed",
        extra={
            "http_method": method,
            "http_path": path,
            "http_status": status_code,
            "duration_ms": duration_ms,
            "user_id": user_id,
        }
    )


def log_error(
        logger: logging.Logger,
        error: Exception,
        context: Optional[dict] = None
) -> None:
    """
    Log an error with context.

    Args:
        logger: Logger instance
        error: Exception that occurred
        context: Additional context dict
    """
    error_data = {
        "error_type": type(error).__name__,
        "error_message": str(error),
    }

    if context:
        error_data.update(context)

    logger.error(
        "Error occurred",
        extra=error_data,
        exc_info=True  # Include stack trace
    )