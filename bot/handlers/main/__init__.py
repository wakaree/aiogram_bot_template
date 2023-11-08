from typing import Final

from aiogram import Router

from . import menu, start

router: Final[Router] = Router(name=__name__)
router.include_routers(start.router, menu.router)
