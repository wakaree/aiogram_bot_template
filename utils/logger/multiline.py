from logging import INFO, Logger, getLogger
from typing import Iterable, Optional


class MultilineLogger:
    def __init__(self, level: int = INFO, logger: Optional[Logger] = None) -> None:
        self.level = level
        self.logger = logger or getLogger()

    def __call__(self, message: Iterable[str]) -> None:
        if isinstance(message, str):
            message = message.splitlines()
        for line in message:
            self.logger.log(self.level, msg=line)
