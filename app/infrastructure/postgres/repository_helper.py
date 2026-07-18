from dataclasses import dataclass
from typing import Any, Optional, Sequence, cast

from sqlalchemy import ColumnExpressionArgument, delete, exists, literal, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption
from sqlalchemy.sql.functions import count

from app.domain.base import Base


@dataclass
class SqlRepositoryHelper[T: Base]:
    session: AsyncSession
    model: type[T]

    async def add_one(self, instance: T) -> None:
        self.session.add(instance)

    async def get_one(
        self,
        *conditions: ColumnExpressionArgument[Any],
        options: Optional[Sequence[ExecutableOption]] = None,
    ) -> Optional[T]:
        query = select(self.model).where(*conditions)
        if options is not None:
            query = query.options(*options)
        return cast(Optional[T], await self.session.scalar(query))

    async def get_many(
        self,
        *conditions: ColumnExpressionArgument[Any],
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        options: Optional[Sequence[ExecutableOption]] = None,
    ) -> list[T]:
        query = select(self.model).where(*conditions)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        if options is not None:
            query = query.options(*options)
        return list(await self.session.scalars(query))

    async def count(self, *conditions: ColumnExpressionArgument[Any]) -> int:
        query = select(count()).select_from(self.model).where(*conditions)
        return cast(int, await self.session.scalar(query) or 0)

    async def exists(self, *conditions: ColumnExpressionArgument[Any]) -> bool:
        query = select(exists(select(literal(1)).select_from(self.model).where(*conditions)))
        return cast(bool, await self.session.scalar(query) or False)

    async def update(self, *conditions: ColumnExpressionArgument[Any], **values: Any) -> int:
        result = await self.session.execute(
            update(self.model).values(**values).where(*conditions),
        )
        return cast(int, result.rowcount or 0)

    async def delete(self, *conditions: ColumnExpressionArgument[Any]) -> int:
        result = await self.session.execute(delete(self.model).where(*conditions))
        return cast(int, result.rowcount or 0)
