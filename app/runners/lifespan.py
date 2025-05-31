from __future__ import annotations

import logging
from typing import Final

from aiogram import Bot
from aiogram_i18n import I18nMiddleware
from fastapi import FastAPI

from app.endpoints.telegram import TelegramRequestHandler
from app.services.redis import RedisRepository

logger: Final[logging.Logger] = logging.getLogger(name=__name__)


async def close_sessions(
    bot: Bot,
    i18n_middleware: I18nMiddleware,
    redis: RedisRepository,
) -> None:
    await i18n_middleware.core.shutdown()
    await bot.session.close()
    await redis.close()
    logger.info("Closed all existing connections")


async def emit_aiogram_shutdown(app: FastAPI) -> None:
    handler: TelegramRequestHandler = app.state.tg_webhook_handler
    await handler.shutdown()
    logger.info("Aiogram shutdown completed")
    app.state.shutdown_completed = True
