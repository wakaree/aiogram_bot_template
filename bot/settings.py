import secrets

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: SecretStr
    use_webhook: bool
    drop_pending_updates: bool
    dev_id: int

    postgres_host: str
    postgres_db: str
    postgres_password: str
    postgres_port: str
    postgres_user: str
    postgres_data: str

    redis_host: str
    redis_port: int
    redis_database: int

    webhook_base_url: str
    webhook_path: str
    webhook_port: int
    webhook_host: str
    webhook_secret_token: str = Field(default_factory=secrets.token_urlsafe)
    reset_webhook: bool

    model_config = SettingsConfigDict(env_file_encoding="utf-8", env_file=".env")

    def build_postgres_dsn(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    def build_webhook_url(self) -> str:
        return f"{self.webhook_base_url}{self.webhook_path}"
