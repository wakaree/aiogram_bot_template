from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from redis.asyncio import ConnectionPool, Redis

from utils import mjson

from .enums import Locale
from .handlers import admin, extra, main
from .middlewares import (
    CommitMiddleware,
    DBSessionMiddleware,
    RetryRequestMiddleware,
    UserAccessMiddleware,
    UserAutoCreationMiddleware,
    UserManager,
)
from .services.database import create_pool

if TYPE_CHECKING:
    from .settings import Settings


def _setup_outer_middlewares(dispatcher: Dispatcher, settings: Settings) -> None:
    db_session_middleware: DBSessionMiddleware = DBSessionMiddleware(
        session_pool=create_pool(dsn=settings.build_postgres_dsn())
    )

    i18n: I18nMiddleware = I18nMiddleware(
        core=FluentRuntimeCore(
            path="translations/{locale}",
            raise_key_error=False,
            locales_map={Locale.RU: Locale.UK, Locale.UK: Locale.EN},
        ),
        manager=UserManager(),
        context_key="l10n",
        default_locale=Locale.DEFAULT,
        middleware_key="l10n_middleware",
    )

    dispatcher.update.outer_middleware(db_session_middleware)
    dispatcher.update.outer_middleware(UserAccessMiddleware())
    i18n.setup(dispatcher=dispatcher)


def _setup_inner_middlewares(dispatcher: Dispatcher) -> None:
    UserAutoCreationMiddleware().setup_inner(router=dispatcher)
    CommitMiddleware().setup_inner(router=dispatcher)
    dispatcher.callback_query.middleware(CallbackAnswerMiddleware())


def create_dispatcher(settings: Settings) -> Dispatcher:
    """
    :return: Configured ``Dispatcher`` with installed middlewares and included routers
    """
    redis: Redis = Redis(
        connection_pool=ConnectionPool(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_database,
        )
    )

    dispatcher: Dispatcher = Dispatcher(
        name="main_dispatcher",
        storage=RedisStorage(redis=redis, json_loads=mjson.decode, json_dumps=mjson.encode),
        redis=redis,
        settings=settings,
    )
    dispatcher.include_routers(admin.router, main.router, extra.router)
    _setup_outer_middlewares(dispatcher=dispatcher, settings=settings)
    _setup_inner_middlewares(dispatcher=dispatcher)
    return dispatcher


def create_bot(settings: Settings) -> Bot:
    """
    :return: Configured ``Bot`` with retry request middleware
    """
    session: AiohttpSession = AiohttpSession(json_loads=mjson.decode, json_dumps=mjson.encode)
    session.middleware(RetryRequestMiddleware())
    return Bot(
        token=settings.bot_token.get_secret_value(),
        parse_mode=ParseMode.HTML,
        session=session,
    )
