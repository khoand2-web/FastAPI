# app/core/logging_config.py
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

from app.core.config import settings


def configure_logging(logfile: Optional[str] = "app.log") -> None:
    """
    Configure root logger for the application.

    Args:
        logfile: path to log file (rotated).
    """
    root = logging.getLogger()
    if root.handlers:
        return
    root.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    )

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    root.addHandler(console)

    if logfile:
        file_handler = RotatingFileHandler(logfile, maxBytes=10 * 1024 * 1024, backupCount=3)
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)
