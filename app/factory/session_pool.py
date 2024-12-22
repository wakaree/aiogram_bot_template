from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.models.config import AppConfig


def create_session_pool(config: AppConfig) -> async_sessionmaker[AsyncSession]:
    engine: AsyncEngine = create_async_engine(
        url=config.postgres.build_url(),
        echo=config.sql_alchemy.echo,
        echo_pool=config.sql_alchemy.echo_pool,
        pool_size=config.sql_alchemy.pool_size,
        max_overflow=config.sql_alchemy.max_overflow,
        pool_timeout=config.sql_alchemy.pool_timeout,
        pool_recycle=config.sql_alchemy.pool_recycle,
    )
    return async_sessionmaker(engine, expire_on_commit=False)
