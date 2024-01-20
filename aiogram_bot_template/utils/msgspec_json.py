from typing import Any, Callable, Final

from msgspec.json import Decoder, Encoder

decode: Final[Callable[..., Any]] = Decoder[dict[str, Any]]().decode
encode_bytes: Final[Callable[..., bytes]] = Encoder().encode


def encode(obj: Any) -> str:
    data: bytes = encode_bytes(obj)
    return data.decode()
