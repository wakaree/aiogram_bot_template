from __future__ import annotations

from typing import AsyncIterator

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.contrib.middlewares import RetryRequestMiddleware
from aiogram.enums import ParseMode
from aiogram.types import LinkPreviewOptions
from dishka import Provider, Scope, provide

from app.application.models.config import AppConfig
from app.utils import mjson


def create_bot(config: AppConfig) -> Bot:
    session: AiohttpSession = AiohttpSession(json_loads=mjson.decode, json_dumps=mjson.encode)
    session.middleware(RetryRequestMiddleware())
    return Bot(
        token=config.telegram.bot_token.get_secret_value(),
        session=session,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview=LinkPreviewOptions(is_disabled=True),
        ),
    )


class BotProvider(Provider):
    scope = Scope.APP

    @provide
    async def provide_bot(self, config: AppConfig) -> AsyncIterator[Bot]:
        bot: Bot = create_bot(config=config)
        yield bot
        await bot.session.close()
