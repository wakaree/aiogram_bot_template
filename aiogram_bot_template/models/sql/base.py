from datetime import datetime
from typing import Annotated, TypeAlias

from sqlalchemy import BigInteger, DateTime, Integer, SmallInteger
from sqlalchemy.orm import DeclarativeBase, registry

Int16: TypeAlias = Annotated[int, 16]
Int32: TypeAlias = Annotated[int, 32]
Int64: TypeAlias = Annotated[int, 64]


class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            Int16: SmallInteger,
            Int32: Integer,
            Int64: BigInteger,
            datetime: DateTime(timezone=True),
        }
    )
