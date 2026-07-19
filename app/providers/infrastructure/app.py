from dishka import Provider, Scope, provide, provide_all

from app.application.models.config import AppConfig, Assets
from app.application.models.config.env import (
    CommonConfig,
    PostgresConfig,
    RedisConfig,
    ServerConfig,
    SQLAlchemyConfig,
    TelegramConfig,
)
from app.infrastructure.telegram.lifespan import LifespanService


def create_app_config() -> AppConfig:
    # noinspection PyArgumentList
    return AppConfig(
        telegram=TelegramConfig(),
        postgres=PostgresConfig(),
        sql_alchemy=SQLAlchemyConfig(),
        redis=RedisConfig(),
        server=ServerConfig(),
        common=CommonConfig(),
    )


class AppInfrastructureProvider(Provider):
    scope = Scope.APP

    infrastructure = provide_all(staticmethod(create_app_config), LifespanService)

    @provide
    def provide_assets(self) -> Assets:
        return Assets()
