from datetime import datetime

from app.const import TIMEZONE


def datetime_now() -> datetime:
    return datetime.now(tz=TIMEZONE)
