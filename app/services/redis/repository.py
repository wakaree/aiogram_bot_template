from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Final, Optional, TypeVar, cast

from pydantic import BaseModel, TypeAdapter
from redis.asyncio import Redis
from redis.typing import ExpiryT

from app.services.redis.keys import WebhookLockKey
from app.utils import mjson
from app.utils.key_builder import StorageKey

if TYPE_CHECKING:
    from app.models.config import AppConfig

T = TypeVar("T", bound=Any)

logger: Final[logging.Logger] = logging.getLogger(name=__name__)
TX_QUEUE_KEY: Final[str] = "tx_queue"


class RedisRepository:
    client: Redis
    config: AppConfig

    def __init__(self, client: Redis, config: AppConfig) -> None:
        self.client = client
        self.config = config

    async def get(
        self,
        key: StorageKey,
        validator: type[T],
        default: Optional[T] = None,
    ) -> Optional[T]:
        value: Optional[Any] = await self.client.get(key.pack())
        if value is None:
            return default
        value = mjson.decode(value)
        return TypeAdapter[T](validator).validate_python(value)

    async def set(self, key: StorageKey, value: Any, ex: Optional[ExpiryT] = None) -> None:
        if isinstance(value, BaseModel):
            value = value.model_dump(exclude_defaults=True)
        await self.client.set(name=key.pack(), value=mjson.encode(value), ex=ex)

    async def exists(self, key: StorageKey) -> bool:
        return cast(bool, await self.client.exists(key.pack()))

    async def delete(self, key: StorageKey) -> None:
        await self.client.delete(key.pack())

    async def close(self) -> None:
        await self.client.aclose(close_connection_pool=True)

    async def is_webhook_set(self, bot_id: int, webhook_hash: str) -> bool:
        key: WebhookLockKey = WebhookLockKey(
            bot_id=bot_id,
            webhook_hash=webhook_hash,
        )
        return await self.exists(key=key)

    async def set_webhook(self, bot_id: int, webhook_hash: str) -> None:
        key: WebhookLockKey = WebhookLockKey(
            bot_id=bot_id,
            webhook_hash=webhook_hash,
        )
        await self.set(key=key, value=None)

    async def clear_webhooks(self, bot_id: int) -> None:
        key: WebhookLockKey = WebhookLockKey(bot_id=bot_id, webhook_hash="*")
        keys: list[bytes] = await self.client.keys(key.pack())
        if not keys:
            return
        await self.client.delete(*keys)
