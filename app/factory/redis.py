from __future__ import annotations

from redis.asyncio import ConnectionPool, Redis

from app.models.config import AppConfig


def create_redis(config: AppConfig) -> Redis:
    return Redis(connection_pool=ConnectionPool.from_url(url=config.redis.build_url()))
