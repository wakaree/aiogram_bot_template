import logging

from .setup import disable_aiogram_logs, setup_logger

__all__ = [
    "database",
    "disable_aiogram_logs",
    "setup_logger",
]

database: logging.Logger = logging.getLogger("bot.database")
