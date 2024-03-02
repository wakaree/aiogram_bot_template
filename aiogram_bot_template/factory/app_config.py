from __future__ import annotations

from ..app_config import AppConfig, CommonConfig, PostgresConfig, RedisConfig, WebhookConfig


def create_app_config() -> AppConfig:
    return AppConfig(
        common=CommonConfig(),
        postgres=PostgresConfig(),
        redis=RedisConfig(),
        webhook=WebhookConfig(),
    )
