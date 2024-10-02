from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from aiogram_bot_template.services.sql import SQLSessionContext


class DBSessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        session_pool: async_sessionmaker[AsyncSession] = data["session_pool"]
        async with SQLSessionContext(session_pool=session_pool) as (repository, uow):
            data["repository"] = repository
            data["uow"] = uow
            return await handler(event, data)
