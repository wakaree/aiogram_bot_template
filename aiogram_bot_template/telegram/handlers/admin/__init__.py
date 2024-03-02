from typing import Final

from aiogram import F, Router

from ...filters import MagicData

router: Final[Router] = Router(name=__name__)
router.message.filter(MagicData(F.chat.id == F.config.common.admin_chat_id))
router.callback_query.filter(MagicData(F.message.chat.id == F.config.common.admin_chat_id))
