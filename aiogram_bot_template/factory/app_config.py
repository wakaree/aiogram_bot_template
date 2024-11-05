from __future__ import annotations

from ..models.config.env import (
    AppConfig,
    CommonConfig,
    PostgresConfig,
    RedisConfig,
    ServerConfig,
    TelegramConfig,
)


def create_app_config() -> AppConfig:
    return AppConfig(
        telegram=TelegramConfig(),
        postgres=PostgresConfig(),
        redis=RedisConfig(),
        server=ServerConfig(),
        common=CommonConfig(),
    )
