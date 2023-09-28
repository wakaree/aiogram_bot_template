from __future__ import annotations

from enum import StrEnum, auto
from typing import Optional


class Locale(StrEnum):
    EN = auto()
    UK = auto()
    RU = auto()

    DEFAULT = EN

    @classmethod
    def resolve(cls, locale: Optional[str] = None) -> Locale:
        if locale not in cls.__members__:
            return Locale.DEFAULT
        return Locale(locale)
