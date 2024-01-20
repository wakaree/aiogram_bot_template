from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def create_pool(dsn: str, enable_logging: bool = False) -> async_sessionmaker[AsyncSession]:
    engine: AsyncEngine = create_async_engine(url=dsn, echo=enable_logging)
    return async_sessionmaker(engine, expire_on_commit=False)
