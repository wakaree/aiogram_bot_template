import logging

from .multiline import MultilineLogger

__all__ = ["database", "webhook", "setup_logger", "MultilineLogger"]

webhook: logging.Logger = logging.getLogger("bot.webhook")
database: logging.Logger = logging.getLogger("bot.database")


def setup_logger(level: int = logging.INFO) -> None:
    for name in ["aiogram.middlewares", "aiogram.event", "aiohttp.access"]:
        logging.getLogger(name).setLevel(logging.WARNING)

    logging.basicConfig(
        format="%(asctime)s %(levelname)s | %(name)s: %(message)s",
        datefmt="[%H:%M:%S]",
        level=level,
    )
