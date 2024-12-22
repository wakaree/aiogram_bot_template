from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sql.base import Base


class UoW:
    session: AsyncSession

    __slots__ = ("session",)

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def commit(self, *instances: Base) -> None:
        self.session.add_all(instances)
        await self.session.commit()

    async def merge(self, *instances: Base) -> None:
        for instance in instances:
            await self.session.merge(instance)

    async def delete(self, *instances: Base) -> None:
        for instance in instances:
            await self.session.delete(instance)
        await self.session.commit()
