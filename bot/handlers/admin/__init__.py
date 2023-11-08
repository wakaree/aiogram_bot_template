from typing import Final

from aiogram import Router

from bot.filters import ADMIN_ONLY

router: Final[Router] = Router(name=__name__)
router.message.filter(ADMIN_ONLY)
router.callback_query.filter(ADMIN_ONLY)
