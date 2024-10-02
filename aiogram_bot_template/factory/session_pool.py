from __future__ import annotations

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def create_session_pool(url: URL) -> async_sessionmaker[AsyncSession]:
    engine: AsyncEngine = create_async_engine(url=url)
    return async_sessionmaker(engine, expire_on_commit=False)
