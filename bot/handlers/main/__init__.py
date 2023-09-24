from aiogram import Router

from . import menu, start

router = Router(name=__name__)
router.include_routers(start.router, menu.router)
