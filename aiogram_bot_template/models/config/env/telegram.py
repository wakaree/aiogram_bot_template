from pydantic import SecretStr, field_validator

from .base import EnvSettings


class TelegramConfig(EnvSettings, env_prefix="TELEGRAM_"):
    bot_token: SecretStr
    locales: str | list[str]
    drop_pending_updates: bool
    use_webhook: bool
    reset_webhook: bool
    webhook_path: str
    webhook_secret: SecretStr

    @field_validator("locales", mode="before")
    def split_locales(cls, value: str | list[str]) -> list[str]:  # noqa: N805
        if isinstance(value, str):
            split_values = [item.strip() for item in value.split(",") if item]
            return split_values
        elif isinstance(value, list):
            return value
        raise ValueError(
            f"Invalid format for TELEGRAM_LOCALES. Value received: {value} (type: {type(value)})"
        )
