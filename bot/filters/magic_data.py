from typing import Any

from aiogram.filters import MagicData as _MagicData
from magic_filter import MagicFilter


class MagicData(_MagicData):
    def __init__(self, magic_data: MagicFilter | Any) -> None:
        if not isinstance(magic_data, MagicFilter):
            raise TypeError(f"Expected MagicFilter got '{type(magic_data).__name__}'")
        super().__init__(magic_data=magic_data)
