from secrets import token_urlsafe

from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings as _BaseSettings
from pydantic_settings import SettingsConfigDict
from sqlalchemy import URL


class BaseSettings(_BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=".env", env_file_encoding="utf-8")


class CommonConfig(BaseSettings, env_prefix="COMMON_"):
    bot_token: SecretStr
    drop_pending_updates: bool
    sqlalchemy_logging: bool
    admin_chat_id: int


class PostgresConfig(BaseSettings, env_prefix="POSTGRES_"):
    host: str
    db: str
    password: SecretStr
    port: int
    user: str
    data: str

    def build_dsn(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.db,
        )


class RedisConfig(BaseSettings, env_prefix="REDIS_"):
    host: str
    port: int
    db: int
    data: str


class WebhookConfig(BaseSettings, env_prefix="WEBHOOK_"):
    use: bool
    reset: bool
    base_url: str
    path: str
    port: int
    host: str
    secret_token: SecretStr = Field(default_factory=token_urlsafe)  # type: ignore[assignment]

    def build_url(self) -> str:
        return f"{self.base_url}{self.path}"


class AppConfig(BaseModel):
    common: CommonConfig
    postgres: PostgresConfig
    redis: RedisConfig
    webhook: WebhookConfig
