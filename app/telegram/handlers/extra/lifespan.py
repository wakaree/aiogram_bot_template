from __future__ import annotations

import logging
from typing import Final

from aiogram import Bot, Router

from app.models.config import Assets
from app.runners.lifespan import close_sessions

logger: Final[logging.Logger] = logging.getLogger(name=__name__)
router: Final[Router] = Router(name=__name__)
router.shutdown.register(close_sessions)


@router.startup()
async def setup_commands(bot: Bot, assets: Assets) -> None:
    for locale, commands in assets.commands.items():
        await bot.set_my_commands(commands=commands, language_code=locale)
