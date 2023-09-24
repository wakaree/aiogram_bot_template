from __future__ import annotations

from os import PathLike
from pathlib import Path
from typing import Any, cast

from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)
from yaml import full_load


class YAMLSettingsConfig(SettingsConfigDict):
    yaml_file: tuple[str | PathLike[str] | Path, ...]


class YAMLSettingsSource(PydanticBaseSettingsSource):
    config: YAMLSettingsConfig

    def get_field_value(self, field: FieldInfo, field_name: str) -> tuple[Any, str, bool]:
        raise NotImplementedError()

    def __call__(self) -> dict[str, Any]:
        data: dict[str, Any] = {}

        for path in self.config["yaml_file"]:
            with open(path, encoding=self.config["env_file_encoding"]) as stream:
                data.update(cast(dict[str, Any], full_load(stream)))

        return data


class YAMLSettings(BaseSettings):
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (YAMLSettingsSource(settings_cls),)
