import time
from datetime import datetime

from app.const import TIMEZONE

START_TIME: int = int(time.time())


def datetime_now() -> datetime:
    return datetime.now(tz=TIMEZONE)


def get_uptime() -> int:
    return int(time.time() - START_TIME)
