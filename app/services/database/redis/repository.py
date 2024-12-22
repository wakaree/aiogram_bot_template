from __future__ import annotations

from typing import Any, Optional, TypeVar

from pydantic import BaseModel, TypeAdapter
from redis.asyncio import Redis
from redis.typing import ExpiryT

from app.models.dto.user import UserDto
from app.utils import mjson
from app.utils.key_builder import StorageKey

from .keys import UserKey

T = TypeVar("T", bound=Any)


class RedisRepository:
    def __init__(self, client: Redis) -> None:
        self.client = client

    async def get(self, key: StorageKey, validator: type[T]) -> Optional[T]:
        value: Optional[Any] = await self.client.get(key.pack())
        if value is None:
            return None
        value = mjson.decode(value)
        return TypeAdapter[T](validator).validate_python(value)

    async def set(self, key: StorageKey, value: Any, ex: Optional[ExpiryT] = None) -> None:
        if isinstance(value, BaseModel):
            value = value.model_dump(exclude_defaults=True)
        await self.client.set(name=key.pack(), value=mjson.encode(value), ex=ex)

    async def delete(self, key: StorageKey) -> None:
        await self.client.delete(key.pack())

    async def close(self) -> None:
        await self.client.aclose(close_connection_pool=True)

    async def save_user(self, key: Any, value: UserDto, cache_time: int) -> None:
        user_key: UserKey = UserKey(key=key)
        await self.set(key=user_key, value=value, ex=cache_time)

    async def get_user(self, key: Any) -> Optional[UserDto]:
        user_key: UserKey = UserKey(key=key)
        return await self.get(key=user_key, validator=UserDto)

    async def delete_user(self, key: Any) -> None:
        user_key: UserKey = UserKey(key=key)
        await self.delete(user_key)
