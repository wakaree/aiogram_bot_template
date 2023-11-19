from dataclasses import dataclass
from typing import Optional

from aiogram.types import User
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from bot.enums import Locale
from bot.models import Base, DBUser


def create_pool(dsn: str) -> async_sessionmaker[AsyncSession]:
    engine: AsyncEngine = create_async_engine(url=dsn)
    return async_sessionmaker(engine, expire_on_commit=False)


@dataclass(kw_only=True)
class Repository:
    session: AsyncSession

    async def get_user(self, pk: int) -> Optional[DBUser]:
        return await self.session.get(entity=DBUser, ident=pk)

    async def create_user(self, user: User) -> DBUser:
        db_user: DBUser = DBUser(
            id=user.id, name=user.full_name, locale=Locale.resolve(user.language_code)
        )
        await self.save(db_user)
        return db_user

    async def save(self, model: Base) -> None:
        self.session.add(model)
        await self.session.commit()
