from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, SmallInteger, String
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy.orm import DeclarativeBase, registry

from app.utils.custom_types import DictStrAny, Int16, Int32, Int64


class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            Int16: SmallInteger(),
            Int32: Integer(),
            Int64: BigInteger(),
            DictStrAny: JSON(),
            list[str]: ARRAY(String()),
            datetime: DateTime(timezone=True),
        }
    )
