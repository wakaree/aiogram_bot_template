from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Optional, TypeVar

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from bot.models import Base


T = TypeVar("T", bound=Base)


class BaseRepository(ABC):
    _session: AsyncSession
    _entity: type[T]

    __slots__ = ("_session", "_entity")

    def __init__(self, session: AsyncSession, entity: type[T]) -> None:
        self._session = session
        self._entity = entity

    async def save(self, model: Base) -> None:
        self._session.add(model)
        await self._session.commit()

    async def get(self, pk: int) -> Optional[T]:
        return await self._session.get(entity=self._entity, ident=pk)

    @abstractmethod
    async def create(self, *args: Any, **kwargs: Any) -> T:
        pass
