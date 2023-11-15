from typing import Any, Callable, Final

from msgspec.json import Decoder, Encoder

decode: Final[Callable[..., Any]] = Decoder[dict[str, Any]]().decode
_encode: Final[Callable[..., bytes]] = Encoder().encode


def encode(obj: Any) -> str:
    data: bytes = _encode(obj)
    return data.decode()
