from __future__ import annotations

from typing import Any, Optional, TypeVar, Union, cast

from sqlalchemy import ColumnExpressionArgument, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from ..uow import UoW

T = TypeVar("T", bound=Any)
ColumnClauseType = Union[
    type[T],
    InstrumentedAttribute[T],
]


# noinspection PyTypeChecker
class BaseRepository:
    session: AsyncSession
    uow: UoW

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.uow = UoW(session=session)

    async def _get(
        self,
        model: ColumnClauseType[T],
        *conditions: ColumnExpressionArgument[Any],
    ) -> Optional[T]:
        return cast(Optional[T], await self.session.scalar(select(model).where(*conditions)))

    async def _get_many(
        self,
        model: ColumnClauseType[T],
        *conditions: ColumnExpressionArgument[Any],
    ) -> list[T]:
        return list(await self.session.scalars(select(model).where(*conditions)))

    async def _update(
        self,
        model: ColumnClauseType[T],
        conditions: list[ColumnExpressionArgument[Any]],
        load_result: bool = True,
        **kwargs: Any,
    ) -> Optional[T]:
        if not kwargs:
            if not load_result:
                return None
            return cast(Optional[T], await self._get(model, *conditions))
        query = update(model).where(*conditions).values(**kwargs)
        if load_result:
            query = query.returning(model)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.scalar_one_or_none() if load_result else None

    async def _delete(
        self,
        model: ColumnClauseType[T],
        *conditions: ColumnExpressionArgument[Any],
    ) -> bool:
        result = await self.session.execute(delete(model).where(*conditions))
        await self.session.commit()
        return cast(bool, result.rowcount > 0)
