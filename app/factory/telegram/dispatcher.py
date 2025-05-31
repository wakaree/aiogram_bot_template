from __future__ import annotations

from aiogram import Dispatcher
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_i18n import I18nMiddleware
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.factory.redis import create_redis
from app.factory.services import create_services
from app.factory.session_pool import create_session_pool
from app.factory.telegram.i18n import create_i18n_middleware
from app.models.config import AppConfig, Assets
from app.telegram.handlers import admin, extra, main
from app.telegram.middlewares import MessageHelperMiddleware, UserMiddleware
from app.utils import mjson


def create_dispatcher(config: AppConfig) -> Dispatcher:
    """
    :return: Configured ``Dispatcher`` with installed middlewares and included routers
    """
    session_pool: async_sessionmaker[AsyncSession] = create_session_pool(config=config)
    redis: Redis = create_redis(config=config)
    i18n_middleware: I18nMiddleware = create_i18n_middleware(config)

    # noinspection PyArgumentList
    dispatcher: Dispatcher = Dispatcher(
        name="main_dispatcher",
        storage=RedisStorage(
            redis=redis,
            key_builder=DefaultKeyBuilder(with_destiny=True),
            json_loads=mjson.decode,
            json_dumps=mjson.encode,
        ),
        config=config,
        assets=Assets(),
        session_pool=session_pool,
        redis=redis,
        **create_services(
            session_pool=session_pool,
            redis=redis,
            config=config,
        ),
    )

    dispatcher.include_routers(admin.router, main.router, extra.router)
    dispatcher.update.outer_middleware(UserMiddleware())
    i18n_middleware.setup(dispatcher=dispatcher)
    dispatcher.update.outer_middleware(MessageHelperMiddleware())
    dispatcher.callback_query.middleware(CallbackAnswerMiddleware())

    return dispatcher
