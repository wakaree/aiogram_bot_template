import logging
import os

from .multiline import MultilineLogger

__all__ = ["database", "webhook", "setup_logger", "MultilineLogger"]

webhook = logging.getLogger("bot.webhook")
database = logging.getLogger("bot.database")


def setup_logger(level: int = logging.INFO) -> None:
    if not os.path.exists("logs"):
        os.mkdir("logs")

    for name in ["aiogram.middlewares", "aiogram.event", "aiohttp.access"]:
        logging.getLogger(name).setLevel(logging.WARNING)

    logging.basicConfig(
        format="%(asctime)s %(levelname)s | %(name)s: %(message)s",
        datefmt="[%H:%M:%S]",
        level=level,
    )
