from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .user import UserRepository


def create_pool(dsn: str) -> async_sessionmaker[AsyncSession]:
    engine: AsyncEngine = create_async_engine(url=dsn)
    return async_sessionmaker(engine, expire_on_commit=False)


class Repository:
    """
    The main repository. Contains all sub-repositories, like for chats, users, etc.
    """

    user: UserRepository

    __slots__ = ("user",)

    def __init__(self, session: AsyncSession) -> None:
        self.user = UserRepository(session=session)
