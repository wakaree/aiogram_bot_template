from __future__ import annotations

from enum import StrEnum, auto


class Locale(StrEnum):
    EN = auto()
    UK = auto()
    RU = auto()

    DEFAULT = EN
