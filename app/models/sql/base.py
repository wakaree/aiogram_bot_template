from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, SmallInteger
from sqlalchemy.orm import DeclarativeBase, registry

from app.utils.custom_types import Int16, Int32, Int64


class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            Int16: SmallInteger,
            Int32: Integer,
            Int64: BigInteger,
            datetime: DateTime(timezone=True),
        }
    )
