from typing import Final

from aiogram import F

from .magic_data import MagicData

ADMIN_FILTER: Final[MagicData] = MagicData(F.event_chat.id == F.config.common.admin_chat_id)

__all__ = ["ADMIN_FILTER", "MagicData"]
