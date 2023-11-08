from typing import Any, Awaitable, Callable, Dict, Final

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.services import Repository

REPOSITORY_KEY: Final[str] = "repository"


class DBSessionMiddleware(BaseMiddleware):
    session_pool: async_sessionmaker[AsyncSession]
    repo_key: str

    def __init__(
        self,
        session_pool: async_sessionmaker[AsyncSession],
        repo_key: str = REPOSITORY_KEY,
    ) -> None:
        self.session_pool = session_pool
        self.repo_key = repo_key

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data[self.repo_key] = Repository(session=session)
            return await handler(event, data)
