from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Bot, Dispatcher, loggers
from aiogram.webhook import aiohttp_server as server
from aiohttp import web

from .utils.loggers import MultilineLogger

if TYPE_CHECKING:
    from .app_config import AppConfig


async def polling_startup(bots: list[Bot], config: AppConfig) -> None:
    for bot in bots:
        await bot.delete_webhook(drop_pending_updates=config.common.drop_pending_updates)
    if config.common.drop_pending_updates:
        loggers.dispatcher.info("Updates skipped successfully")


async def webhook_startup(dispatcher: Dispatcher, bot: Bot, config: AppConfig) -> None:
    url: str = config.webhook.build_url()
    if await bot.set_webhook(
        url=url,
        allowed_updates=dispatcher.resolve_used_update_types(),
        secret_token=config.webhook.secret_token.get_secret_value(),
        drop_pending_updates=config.common.drop_pending_updates,
    ):
        return loggers.webhook.info("Main bot webhook successfully set on url '%s'", url)
    return loggers.webhook.error("Failed to set main bot webhook on url '%s'", url)


async def webhook_shutdown(bot: Bot, config: AppConfig) -> None:
    if not config.webhook.reset:
        return
    if await bot.delete_webhook():
        loggers.webhook.info("Dropped main bot webhook.")
    else:
        loggers.webhook.error("Failed to drop main bot webhook.")
    await bot.session.close()


def run_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    dispatcher.startup.register(polling_startup)
    return dispatcher.run_polling(bot)


def run_webhook(dispatcher: Dispatcher, bot: Bot, config: AppConfig) -> None:
    app: web.Application = web.Application()
    server.SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
        secret_token=config.webhook.secret_token.get_secret_value(),
    ).register(app, path=config.webhook.path)
    server.setup_application(app, dispatcher, bot=bot)
    app.update(**dispatcher.workflow_data, bot=bot)
    dispatcher.startup.register(webhook_startup)
    dispatcher.shutdown.register(webhook_shutdown)

    return web.run_app(
        app=app,
        host=config.webhook.host,
        port=config.webhook.port,
        print=MultilineLogger(),
    )
