from typing import Any, Awaitable, Callable, Final

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.services import Repository

REPOSITORY_KEY: Final[str] = "repository"


class DBSessionMiddleware(BaseMiddleware):
    session_pool: async_sessionmaker[AsyncSession]
    repository_key: str

    __slots__ = ("session_pool", "repository_key")

    def __init__(
        self,
        session_pool: async_sessionmaker[AsyncSession],
        repository_key: str = REPOSITORY_KEY,
    ) -> None:
        self.session_pool = session_pool
        self.repository_key = repository_key

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data[self.repository_key] = Repository(session=session)
            return await handler(event, data)
