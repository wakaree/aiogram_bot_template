from typing import Final

from aiogram import F
from aiogram.enums import ChatType
from aiogram.filters import Filter

from .magic_data import MagicData

ADMIN_ONLY: Final[Filter] = MagicData(F.event_from_user.id == F.config.id)
PRIVATE_ONLY: Final[Filter] = MagicData(F.event_chat.type == ChatType.PRIVATE)
