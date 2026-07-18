from typing import AsyncIterator

from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from dishka import Provider, Scope, provide
from redis.asyncio import ConnectionPool, Redis

from app.application.models.config import AppConfig
from app.application.ports.storages.cache import Cache
from app.application.ports.storages.key_value import KvStorage
from app.infrastructure.redis.cache.service import RedisCache
from app.infrastructure.redis.repository import RedisRepository
from app.utils import mjson


class RedisProvider(Provider):
    scope = Scope.APP

    @provide
    async def provide_redis(self, config: AppConfig) -> AsyncIterator[Redis]:
        redis: Redis = Redis(connection_pool=ConnectionPool.from_url(url=config.redis.build_url()))
        yield redis
        await redis.aclose(close_connection_pool=True)

    @provide
    def provide_cache(self, redis: Redis) -> Cache:
        return RedisCache(_redis=redis)

    @provide
    def provide_redis_repository(self, redis: Redis) -> RedisRepository:
        return RedisRepository(client=redis)

    @provide
    def provide_kv_storage(self, repository: RedisRepository) -> KvStorage:
        return repository

    @provide
    def provide_fsm_storage(self, redis: Redis) -> RedisStorage:
        return RedisStorage(
            redis=redis,
            key_builder=DefaultKeyBuilder(with_destiny=True),
            json_loads=mjson.decode,
            json_dumps=mjson.encode,
        )
