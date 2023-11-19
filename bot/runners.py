from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Bot, Dispatcher, loggers
from aiogram.webhook import aiohttp_server as server
from aiohttp import web

from utils.loggers import MultilineLogger

if TYPE_CHECKING:
    from .settings import Settings


async def polling_startup(bots: list[Bot], settings: Settings) -> None:
    for bot in bots:
        await bot.delete_webhook(drop_pending_updates=settings.drop_pending_updates)
    if settings.drop_pending_updates:
        loggers.dispatcher.info("Updates skipped successfully")


async def webhook_startup(dispatcher: Dispatcher, bot: Bot, settings: Settings) -> None:
    url: str = settings.build_webhook_url()
    if await bot.set_webhook(
        url=url,
        allowed_updates=dispatcher.resolve_used_update_types(),
        secret_token=settings.webhook_secret_token,
        drop_pending_updates=settings.drop_pending_updates,
    ):
        return loggers.webhook.info("Bot webhook successfully set on url '%s'", url)
    return loggers.webhook.error("Failed to set main bot webhook on url '%s'", url)


async def webhook_shutdown(bot: Bot, settings: Settings) -> None:
    if not settings.reset_webhook:
        return
    if await bot.delete_webhook():
        loggers.webhook.info("Dropped main bot webhook.")
    else:
        loggers.webhook.error("Failed to drop main bot webhook.")
    await bot.session.close()


def run_polling(dp: Dispatcher, bot: Bot) -> None:
    dp.startup.register(polling_startup)
    return dp.run_polling(bot)


def run_webhook(dp: Dispatcher, bot: Bot, settings: Settings) -> None:
    app: web.Application = web.Application()
    dp.startup.register(webhook_startup)
    dp.shutdown.register(webhook_shutdown)

    server.SimpleRequestHandler(
        dispatcher=dp, bot=bot, secret_token=settings.webhook_secret_token
    ).register(app, path=settings.webhook_path)
    server.setup_application(app, dp, bot=bot, reset_webhook=settings.reset_webhook)

    return web.run_app(
        app=app,
        host=settings.webhook_host,
        port=settings.webhook_port,
        print=MultilineLogger(),
    )
