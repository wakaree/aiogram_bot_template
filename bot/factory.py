from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from redis.asyncio import Redis

from utils import mjson

from .enums import Locale
from .handlers import admin, extra, main
from .middlewares import (
    CommitMiddleware,
    DBSessionMiddleware,
    RetryRequestMiddleware,
    UserManager,
    UserMiddleware,
)
from .services import create_pool
from .settings import Settings


def create_dispatcher() -> Dispatcher:
    redis: Redis = Redis()

    dp: Dispatcher = Dispatcher(
        name="main_dispatcher",
        storage=RedisStorage(redis=redis, json_loads=mjson.decode, json_dumps=mjson.encode),
        redis=redis,
    )
    dp["settings"] = settings = Settings()
    dp.include_routers(admin.router, main.router, extra.router)

    dp.update.outer_middleware(DBSessionMiddleware(session_pool=create_pool(dsn=settings.dsn)))
    dp.update.outer_middleware(UserMiddleware())

    l10n: I18nMiddleware = I18nMiddleware(
        core=FluentRuntimeCore(
            path="translations/{locale}",
            raise_key_error=False,
            locales_map={Locale.RU: Locale.UK, Locale.UK: Locale.EN},
        ),
        manager=UserManager(),
        context_key="l10n",
        middleware_key="l10n_middleware",
        default_locale=Locale.DEFAULT,
    )
    l10n.setup(dp)

    CommitMiddleware().setup(dp)
    dp.callback_query.middleware(CallbackAnswerMiddleware())

    return dp


def create_bot(settings: Settings) -> Bot:
    session: AiohttpSession = AiohttpSession(json_loads=mjson.decode, json_dumps=mjson.encode)
    session.middleware(RetryRequestMiddleware())
    return Bot(
        token=settings.api_token.get_secret_value(),
        parse_mode=ParseMode.HTML,
        session=session,
    )
