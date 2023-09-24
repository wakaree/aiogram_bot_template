from aiogram import Router

from . import errors, pm

router = Router(name=__name__)
router.include_routers(errors.router, pm.router)
