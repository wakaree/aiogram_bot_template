from typing import Final

from aiogram import Router

from app.telegram.filters import ADMIN_FILTER

router: Final[Router] = Router(name=__name__)
router.message.filter(ADMIN_FILTER)
router.callback_query.filter(ADMIN_FILTER)
