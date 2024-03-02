from __future__ import annotations

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from ..app_config import AppConfig
from ..middlewares import RetryRequestMiddleware
from ..utils import msgspec_json as mjson


def create_bot(config: AppConfig) -> Bot:
    """
    :return: Configured ``Bot`` with retry request middleware
    """
    session: AiohttpSession = AiohttpSession(json_loads=mjson.decode, json_dumps=mjson.encode)
    session.middleware(RetryRequestMiddleware())
    return Bot(
        token=config.common.bot_token.get_secret_value(),
        parse_mode=ParseMode.HTML,
        session=session,
    )
