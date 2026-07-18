from typing import Any

from dishka import AsyncContainer, make_async_container
from dishka.provider import BaseProvider

from app.providers.handling.flows import FlowsProvider
from app.providers.handling.interactors import InteractorsProvider
from app.providers.handling.presenters import PresentersProvider
from app.providers.infrastructure.app import AppInfrastructureProvider
from app.providers.infrastructure.i18n import I18nProvider, UserLocaleProvider
from app.providers.infrastructure.postgres import PostgresProvider
from app.providers.infrastructure.redis import RedisProvider
from app.providers.infrastructure.repositories import RepositoriesProvider
from app.providers.infrastructure.request import (
    MessageHelperProvider,
    RequestInfrastructureProvider,
    UserProvider,
)
from app.providers.telegram.bot import BotProvider


def create_container(
    *providers: BaseProvider,
    context: dict[type[Any], Any] | None = None,
) -> AsyncContainer:
    return make_async_container(
        AppInfrastructureProvider(),
        BotProvider(),
        PostgresProvider(),
        RedisProvider(),
        RepositoriesProvider(),
        UserProvider(),
        MessageHelperProvider(),
        RequestInfrastructureProvider(),
        I18nProvider(),
        UserLocaleProvider(),
        InteractorsProvider(),
        PresentersProvider(),
        FlowsProvider(),
        *providers,
        context=context,
    )
