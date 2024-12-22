from pydantic_settings import BaseSettings, SettingsConfigDict

from app.const import ENV_FILE


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
    )
