from __future__ import annotations

from typing import Dict

from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore

from .app_config import AppConfig
from ..const import DEFAULT_LOCALE, MESSAGES_SOURCE_DIR
from ..telegram.middlewares.outer import UserManager


def create_i18n_core(config: AppConfig) -> FluentRuntimeCore:
    # Creating a map
    locales = config.telegram.locales
    locales_map: Dict[str, str] = {locales[i]: locales[i + 1] for i in range(len(locales) - 1)}

    return FluentRuntimeCore(
        path=MESSAGES_SOURCE_DIR / "{locale}",
        raise_key_error=False,
        locales_map=locales_map,
    )


def create_i18n_middleware(config: AppConfig) -> I18nMiddleware:
    return I18nMiddleware(
        core=create_i18n_core(config=config),
        manager=UserManager(),
        default_locale=DEFAULT_LOCALE,
    )
