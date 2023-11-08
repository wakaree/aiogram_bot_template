from typing import Final

from aiogram import Router

from . import errors, pm

router: Final[Router] = Router(name=__name__)
router.include_routers(errors.router, pm.router)
