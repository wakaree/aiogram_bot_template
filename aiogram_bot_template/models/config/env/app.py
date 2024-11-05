from pydantic import BaseModel

from .common import CommonConfig
from .postgres import PostgresConfig
from .redis import RedisConfig
from .server import ServerConfig
from .telegram import TelegramConfig


class AppConfig(BaseModel):
    telegram: TelegramConfig
    postgres: PostgresConfig
    redis: RedisConfig
    server: ServerConfig
    common: CommonConfig
