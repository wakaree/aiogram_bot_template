from __future__ import annotations

from typing import Any, Optional, TypeVar

from pydantic import BaseModel, TypeAdapter
from redis.asyncio import Redis
from redis.typing import ExpiryT

from ...utils import mjson

T = TypeVar("T", bound=Any)


class RedisRepository:
    def __init__(self, client: Redis) -> None:
        self.client = client

    async def get(self, key: str, validator: type[T]) -> Optional[T]:
        value: Optional[Any] = await self.client.get(key)
        if value is None:
            return None
        value = mjson.decode(value)
        return TypeAdapter[T](validator).validate_python(value)

    async def set(self, key: str, value: Any, ex: Optional[ExpiryT] = None) -> None:
        if isinstance(value, BaseModel):
            value = value.model_dump(exclude_defaults=True)
        await self.client.set(name=key, value=mjson.encode(value), ex=ex)

    async def delete(self, key: str) -> None:
        await self.client.delete(key)

    async def close(self) -> None:
        await self.client.aclose(close_connection_pool=True)
