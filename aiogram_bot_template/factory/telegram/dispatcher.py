from __future__ import annotations

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_i18n import I18nMiddleware
from redis.asyncio import Redis

from ...models.config import AppConfig
from ...services.redis.repository import RedisRepository
from ...telegram.handlers import admin, common, extra
from ...telegram.middlewares.outer import DBSessionMiddleware, UserMiddleware
from ...utils import mjson
from ..redis import create_redis
from ..session_pool import create_session_pool
from .i18n import create_i18n_middleware


def create_dispatcher(config: AppConfig) -> Dispatcher:
    """
    :return: Configured ``Dispatcher`` with installed middlewares and included routers
    """
    redis: Redis = create_redis(url=config.redis.build_url())
    i18n_middleware: I18nMiddleware = create_i18n_middleware(config)

    dispatcher: Dispatcher = Dispatcher(
        name="main_dispatcher",
        storage=RedisStorage(
            redis=redis,
            json_loads=mjson.decode,
            json_dumps=mjson.encode,
        ),
        config=config,
        session_pool=create_session_pool(url=config.postgres.build_url()),
        redis=RedisRepository(client=redis),
    )

    dispatcher.include_routers(admin.router, common.router, extra.router)
    dispatcher.update.outer_middleware(DBSessionMiddleware())
    dispatcher.update.outer_middleware(UserMiddleware())
    i18n_middleware.setup(dispatcher=dispatcher)
    dispatcher.callback_query.middleware(CallbackAnswerMiddleware())

    return dispatcher
