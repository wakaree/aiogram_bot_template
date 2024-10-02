from __future__ import annotations

from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore

from ..const import DEFAULT_LOCALE, MESSAGES_SOURCE_DIR
from ..enums import Locale
from ..telegram.middlewares.outer import UserManager


def create_i18n_core() -> FluentRuntimeCore:
    return FluentRuntimeCore(
        path=MESSAGES_SOURCE_DIR / "{locale}",
        raise_key_error=False,
        locales_map={Locale.RU: Locale.UK, Locale.UK: Locale.EN},
    )


def create_i18n_middleware() -> I18nMiddleware:
    return I18nMiddleware(
        core=create_i18n_core(),
        manager=UserManager(),
        default_locale=DEFAULT_LOCALE,
    )
