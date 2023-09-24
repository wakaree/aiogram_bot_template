from aiogram import F
from aiogram.enums import ChatType

from .magic_data import MagicData

ADMIN_ONLY = MagicData(F.event_from_user.id == F.config.id)
PRIVATE_ONLY = MagicData(F.event_chat.type == ChatType.PRIVATE)
