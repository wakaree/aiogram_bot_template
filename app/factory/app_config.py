from __future__ import annotations

from app.models.config.env import (
    AppConfig,
    CommonConfig,
    PostgresConfig,
    RedisConfig,
    ServerConfig,
    SQLAlchemyConfig,
    TelegramConfig,
)


# noinspection PyArgumentList
def create_app_config() -> AppConfig:
    return AppConfig(
        telegram=TelegramConfig(),
        postgres=PostgresConfig(),
        sql_alchemy=SQLAlchemyConfig(),
        redis=RedisConfig(),
        server=ServerConfig(),
        common=CommonConfig(),
    )
