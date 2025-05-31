from typing import Final

from aiogram import Router

from . import errors, lifespan, pm

router: Final[Router] = Router(name=__name__)
router.include_routers(errors.router, lifespan.router, pm.router)
