from dataclasses import dataclass
from typing import Optional

from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from bot.models import Base, DBUser


def create_pool(dsn: PostgresDsn) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(url=dsn.unicode_string())
    maker = async_sessionmaker(engine, expire_on_commit=False)

    return maker


@dataclass(kw_only=True)
class Repository:
    session: AsyncSession

    async def get_user(self, pk: int) -> Optional[DBUser]:
        return await self.session.get(entity=DBUser, ident=pk)

    async def save(self, model: Base) -> None:
        self.session.add(model)
        await self.session.commit()
