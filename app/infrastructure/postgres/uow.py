from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.base import Base


@dataclass(slots=True)
class UoW:
    session: AsyncSession

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
