from typing import Final

from aiogram import F, Router

from bot.filters import MagicData

router: Final[Router] = Router(name=__name__)
router.message.filter(MagicData(F.chat.id == F.config.admin_chat_id))
router.callback_query.filter(MagicData(F.message.chat.id == F.config.admin_chat_id))
