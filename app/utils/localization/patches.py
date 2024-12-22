from typing import Any, Optional

from fluent.runtime.types import FluentNumber, FluentType, NumberFormatOptions

FluentNumber.default_number_format_options = NumberFormatOptions(useGrouping=False)


class FluentBool(FluentType):
    def __init__(self, value: Any) -> None:
        self.value = bool(value)

    def format(self, *_: Any) -> str:
        if self.value:
            return "true"
        return "false"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.format() == other
        return False


class FluentNullable(FluentType):
    def __init__(self, value: Optional[Any] = None) -> None:
        self.value = value

    def format(self, *_: Any) -> str:
        if self.value is not None:
            return str(self.value)
        return "null"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.format() == other
        return False
