from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.contrib.middlewares import RetryRequestMiddleware
from aiogram.enums import ParseMode

from ...utils import mjson

if TYPE_CHECKING:
    from ...models.config import AppConfig


def create_bot(config: AppConfig) -> Bot:
    session: AiohttpSession = AiohttpSession(json_loads=mjson.decode, json_dumps=mjson.encode)
    session.middleware(RetryRequestMiddleware())
    return Bot(
        token=config.telegram.bot_token.get_secret_value(),
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
