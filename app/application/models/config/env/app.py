from pydantic import BaseModel

from .common import CommonConfig
from .postgres import PostgresConfig
from .redis import RedisConfig
from .server import ServerConfig
from .sql_alchemy import SQLAlchemyConfig
from .telegram import TelegramConfig


class AppConfig(BaseModel):
    telegram: TelegramConfig
    postgres: PostgresConfig
    sql_alchemy: SQLAlchemyConfig
    redis: RedisConfig
    server: ServerConfig
    common: CommonConfig
