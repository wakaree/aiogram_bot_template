import secrets

from pydantic import BaseModel, Field, PostgresDsn, SecretStr

from utils.yaml_reader import YAMLSettings, YAMLSettingsConfig


class Webhook(BaseModel):
    base_url: str
    path: str
    port: int
    host: str
    secret_token: str = Field(default_factory=secrets.token_urlsafe)

    def build_url(self) -> str:
        return f"{self.base_url}{self.path}"


class Settings(YAMLSettings):
    api_token: SecretStr
    dsn: PostgresDsn
    dev_id: int

    webhook: Webhook

    model_config = YAMLSettingsConfig(env_file_encoding="utf-8", yaml_file=("config.yml",))
