from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.models.config import AppConfig
from app.services.base import BaseService


class CrudService(BaseService):
    session_pool: async_sessionmaker[AsyncSession]
    redis: Redis
    config: AppConfig

    def __init__(
        self,
        session_pool: async_sessionmaker[AsyncSession],
        redis: Redis,
        config: AppConfig,
    ) -> None:
        super().__init__()
        self.session_pool = session_pool
        self.redis = redis
        self.config = config
