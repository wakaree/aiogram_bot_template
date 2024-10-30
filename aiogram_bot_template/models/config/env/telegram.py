from typing import Any

from pydantic import SecretStr, field_validator

from .base import EnvSettings


class TelegramConfig(EnvSettings, env_prefix="TELEGRAM_"):
    bot_token: SecretStr
    locales: str | list[str]
    admin_ids: int | list[int]
    drop_pending_updates: bool
    use_webhook: bool
    reset_webhook: bool
    webhook_path: str
    webhook_secret: SecretStr

    @field_validator("locales", "admin_ids", mode="before")
    def split_and_convert(cls, value: Any, info) -> list[str] | list[int]:  # type: ignore
        if isinstance(value, str):
            split_values = [item.strip() for item in value.split(",") if item]
        elif isinstance(value, int) and info.field_name == "admin_ids":
            return [value]
        elif isinstance(value, list):
            split_values = value
        else:
            raise ValueError(
                f"Invalid format for {info.field_name.upper()}. "
                f"Value received: {value} (type: {type(value)})"
            )

        if info.field_name == "admin_ids":
            try:
                split_values_int = [int(item) for item in split_values]
                return split_values_int
            except ValueError:
                raise ValueError(
                    f"Invalid format for TELEGRAM_ADMIN_IDS. All values must be integers."
                )

        return split_values
