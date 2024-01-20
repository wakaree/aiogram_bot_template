from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from ..models import Base


class BaseRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self, *instances: Base) -> None:
        self._session.add_all(instances)
        await self._session.commit()
