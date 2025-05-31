from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, AsyncGenerator

from aiogram import Bot, Dispatcher, loggers
from fastapi import FastAPI

if TYPE_CHECKING:
    from app.models.config import AppConfig


async def polling_startup(bots: list[Bot], config: AppConfig) -> None:
    for bot in bots:
        await bot.delete_webhook(drop_pending_updates=config.telegram.drop_pending_updates)
    if config.telegram.drop_pending_updates:
        loggers.dispatcher.info("Updates skipped successfully")


# noinspection PyProtectedMember
@asynccontextmanager
async def polling_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    dispatcher: Dispatcher = app.state.dispatcher
    bot: Bot = app.state.bot
    asyncio.create_task(dispatcher.start_polling(bot, handle_signals=False))
    yield
    if dispatcher._running_lock.locked():
        await dispatcher.stop_polling()
