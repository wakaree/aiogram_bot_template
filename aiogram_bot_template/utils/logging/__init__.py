import logging

from .multiline import MultilineLogger
from .setup import disable_aiogram_logs, setup_logger

__all__ = [
    "MultilineLogger",
    "database",
    "disable_aiogram_logs",
    "setup_logger",
]


database: logging.Logger = logging.getLogger("bot.database")
