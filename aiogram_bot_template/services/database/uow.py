from sqlalchemy.ext.asyncio import AsyncSession

from .models import Base


class UoW:
    _session: AsyncSession

    __slots__ = ("_session",)

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self, *instances: Base) -> None:
        self._session.add_all(instances)
        await self._session.commit()

    async def delete(self, *instances: Base) -> None:
        for instance in instances:
            await self._session.delete(instance)
        await self._session.commit()
