"""
logger.py — Centralized logging for YouTube Auto-Downloader
Logs are printed to the console with timestamps and severity levels.
"""

import logging
import sys
from datetime import datetime


def setup_logger(name: str = "YTDownloader") -> logging.Logger:
    """
    Creates and returns a configured logger instance.
    Outputs clean, timestamped logs to the console.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


# Single shared logger instance used across the project
logger = setup_logger()