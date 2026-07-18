from typing import AsyncGenerator, NewType, cast

from aiogram.types import TelegramObject
from aiogram_i18n import I18nContext
from aiogram_i18n.cores import FluentRuntimeCore
from aiogram_i18n.managers import BaseManager
from dishka import Provider, Scope, provide
from dishka.integrations.aiogram import AiogramMiddlewareData, AiogramProvider

from app.application.models.config import AppConfig
from app.const import DEFAULT_LOCALE, MESSAGES_SOURCE_DIR
from app.infrastructure.localization.manager import UserManager

UserLocale = NewType("UserLocale", str)


def create_i18n_core(config: AppConfig) -> FluentRuntimeCore:
    locales: list[str] = config.telegram.locales
    return FluentRuntimeCore(
        path=MESSAGES_SOURCE_DIR / "{locale}",
        raise_key_error=False,
        locales_map={locales[i]: locales[i + 1] for i in range(len(locales) - 1)},
    )


class UserLocaleProvider(AiogramProvider):
    @provide(scope=Scope.REQUEST)
    async def provide_user_locale(
        self,
        event: TelegramObject,
        middleware_data: AiogramMiddlewareData,
        core: FluentRuntimeCore,
        manager: BaseManager,
    ) -> UserLocale:
        locale: str = await manager.locale_getter(event=event, **middleware_data)
        if locale not in core.available_locales:
            return UserLocale(cast(str, core.default_locale))
        return UserLocale(locale)


class I18nProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_i18n_core(
        self,
        config: AppConfig,
    ) -> AsyncGenerator[FluentRuntimeCore, None]:
        core = create_i18n_core(config=config)
        await core.startup()
        yield core
        await core.shutdown()

    @provide(scope=Scope.APP)
    async def provide_i18n_manager(self) -> BaseManager:
        return UserManager(default_locale=DEFAULT_LOCALE)

    @provide(scope=Scope.REQUEST)
    async def provide_i18n_context(
        self,
        user_locale: UserLocale,
        core: FluentRuntimeCore,
        manager: BaseManager,
        middleware_data: AiogramMiddlewareData,
    ) -> I18nContext:
        context = cast(I18nContext | None, middleware_data.get("i18n"))
        if context is not None:
            return context

        current_context = cast(I18nContext | None, I18nContext.get_current())
        if current_context is not None:
            return current_context

        return I18nContext(
            locale=user_locale,
            core=core,
            manager=manager,
            data=middleware_data,
            key_separator="-",
        )
