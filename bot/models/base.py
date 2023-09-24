from typing import Annotated

from sqlalchemy import BigInteger, Integer
from sqlalchemy.orm import DeclarativeBase, registry

Int16 = Annotated[int, 16]
Int64 = Annotated[int, 64]


class Base(DeclarativeBase):
    registry = registry(type_annotation_map={Int16: Integer, Int64: BigInteger})
