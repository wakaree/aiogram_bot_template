from typing import Final

from aiogram import Router

from . import menu

router: Final[Router] = Router(name=__name__)
router.include_routers(menu.router)
