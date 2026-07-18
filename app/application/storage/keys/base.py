from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
from typing import Any, ClassVar, cast
from uuid import UUID

from pydantic import TypeAdapter


@dataclass(frozen=True, slots=True)
class StorageKey[T]:
    __separator__: ClassVar[str]
    __prefix__: ClassVar[str | None]
    __value_type__: ClassVar[TypeAdapter[Any]]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        separator = kwargs.pop("separator", ":")
        prefix = kwargs.pop("prefix", None)
        value_type = kwargs.pop("type", Any)

        cls.__separator__ = separator
        cls.__prefix__ = prefix
        cls.__value_type__ = TypeAdapter[T](value_type)

        if cls.__separator__ in (cls.__prefix__ or ""):
            raise ValueError(
                f"Separator symbol {cls.__separator__!r} can not be used "
                f"inside prefix {cls.__prefix__!r}"
            )
        # Zero-arg super() would resolve `__class__` via a closure cell bound at
        # class-body compile time, but `@dataclass(slots=True)` rebuilds this
        # class into a new object afterwards, leaving that cell stale — hence
        # the explicit two-arg form.
        super(StorageKey, cls).__init_subclass__(**kwargs)

    @classmethod
    def encode_value(cls, value: Any) -> str:
        if value is None:
            return "null"
        if isinstance(value, Enum):
            return str(value.value)
        if isinstance(value, UUID):
            return value.hex
        if isinstance(value, bool):
            return str(int(value))
        return str(value)

    def _iter_items(self) -> list[tuple[str, Any]]:
        if not is_dataclass(self):
            raise TypeError("StorageKey subclasses must be dataclasses")

        return [(f.name, getattr(self, f.name)) for f in fields(self)]

    def pack(self) -> str:
        parts: list[str] = [self.__prefix__] if self.__prefix__ else []

        for key, value in self._iter_items():
            encoded = self.encode_value(value)
            if self.__separator__ in encoded:
                raise ValueError(
                    f"Separator symbol {self.__separator__!r} can not be used "
                    f"in value {key}={encoded!r}"
                )
            parts.append(encoded)

        return self.__separator__.join(parts)

    def validate_value(self, value: Any) -> T:
        return cast(T, self.__value_type__.validate_python(value))
