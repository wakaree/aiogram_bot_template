from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Optional, cast

from pydantic import BaseModel
from redis.asyncio import Redis
from redis.typing import ExpiryT

from app.application.ports.storages.key_value import KvStorage
from app.application.storage.keys.base import StorageKey
from app.application.storage.keys.impl import CommandsLockKey, WebhookLockKey
from app.utils import mjson

# Обновляются на каждом старте, поэтому TTL — просто garbage collection
# записей для ботов, которые больше не поднимаются.
_LOCK_TTL: timedelta = timedelta(days=30)


@dataclass
class RedisRepository(KvStorage):
    client: Redis

    async def get[T](self, key: StorageKey[T]) -> Optional[T]:
        value: Optional[Any] = await self.client.get(key.pack())
        if value is None:
            return None
        return key.validate_value(mjson.decode(value))

    async def set(self, key: StorageKey[Any], value: Any, ex: Optional[ExpiryT] = None) -> None:
        if isinstance(value, BaseModel):
            value = value.model_dump(exclude_defaults=True)
        await self.client.set(name=key.pack(), value=mjson.encode(value), ex=ex)

    async def exists(self, key: StorageKey[Any]) -> bool:
        return cast(bool, await self.client.exists(key.pack()))

    async def delete(self, key: StorageKey[Any]) -> None:
        await self.client.delete(key.pack())

    async def close(self) -> None:
        await self.client.aclose(close_connection_pool=True)

    async def is_webhook_set(self, bot_id: int, webhook_hash: str) -> bool:
        stored_hash: Optional[str] = await self.get(key=WebhookLockKey(bot_id=bot_id))
        return stored_hash == webhook_hash

    async def set_webhook(self, bot_id: int, webhook_hash: str) -> None:
        await self.set(key=WebhookLockKey(bot_id=bot_id), value=webhook_hash, ex=_LOCK_TTL)

    async def clear_webhooks(self, bot_id: int) -> None:
        await self.delete(key=WebhookLockKey(bot_id=bot_id))

    async def is_commands_set(self, bot_id: int, commands_hash: str) -> bool:
        stored_hash: Optional[str] = await self.get(key=CommandsLockKey(bot_id=bot_id))
        return stored_hash == commands_hash

    async def set_commands_lock(self, bot_id: int, commands_hash: str) -> None:
        await self.set(key=CommandsLockKey(bot_id=bot_id), value=commands_hash, ex=_LOCK_TTL)
