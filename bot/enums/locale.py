from __future__ import annotations

from contextlib import suppress
from enum import StrEnum, auto
from typing import Optional


class Locale(StrEnum):
    EN = auto()
    UK = auto()
    RU = auto()

    DEFAULT = EN

    @classmethod
    def resolve(cls, locale: Optional[str] = None) -> Locale:
        if locale is None:
            return Locale.DEFAULT
        with suppress(ValueError):
            return Locale(locale)
        return Locale.DEFAULT
