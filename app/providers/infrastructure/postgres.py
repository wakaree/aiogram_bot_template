from typing import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.application.models.config import AppConfig


class PostgresProvider(Provider):
    scope = Scope.APP

    @provide
    async def provide_engine(self, config: AppConfig) -> AsyncIterator[AsyncEngine]:
        engine: AsyncEngine = create_async_engine(
            url=config.postgres.build_url(),
            echo=config.sql_alchemy.echo,
            echo_pool=config.sql_alchemy.echo_pool,
            pool_size=config.sql_alchemy.pool_size,
            max_overflow=config.sql_alchemy.max_overflow,
            pool_timeout=config.sql_alchemy.pool_timeout,
            pool_recycle=config.sql_alchemy.pool_recycle,
        )
        yield engine
        await engine.dispose()

    @provide
    def provide_session_pool(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def provide_session(
        self,
        session_pool: async_sessionmaker[AsyncSession],
    ) -> AsyncIterator[AsyncSession]:
        async with session_pool() as session:
            yield session
