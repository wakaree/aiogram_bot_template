from typing import cast

import click
from aiogram import Bot, Dispatcher, loggers
from aiogram.webhook import aiohttp_server as server
from aiohttp import web

from utils.loggers import MultilineLogger, setup_logger

from .factory import create_bot, create_dispatcher
from .settings import Settings


async def webhook_startup(dispatcher: Dispatcher, bot: Bot, settings: Settings) -> None:
    url: str = settings.webhook.build_url()
    await bot.delete_webhook()
    if await bot.set_webhook(
        url=url,
        allowed_updates=dispatcher.resolve_used_update_types(),
        secret_token=settings.webhook.secret_token,
    ):
        return loggers.webhook.info("Bot webhook successfully set on url '%s'", url)
    return loggers.webhook.error("Failed to set main bot webhook on url '%s'", url)


async def webhook_shutdown(bot: Bot, reset_webhook: bool) -> None:
    async with bot.session:
        if reset_webhook:
            if await bot.delete_webhook():
                loggers.webhook.info("Dropped main bot webhook.")
                return
            loggers.webhook.error("Failed to drop main bot webhook.")


async def drop_pending_updates(bots: list[Bot]) -> None:
    for bot in bots:
        await bot.delete_webhook(drop_pending_updates=True)
    loggers.dispatcher.info("Updates skipped successfully")


@click.group("cli")
def cli() -> None:
    setup_logger()


@cli.command("polling")
@click.option("-s", "--skip-updates", is_flag=True, default=False)
def run_polling(skip_updates: bool) -> None:
    dp: Dispatcher = create_dispatcher()
    bot: Bot = create_bot(settings=cast(Settings, dp["settings"]))
    if skip_updates:
        dp.startup.register(drop_pending_updates)
    return dp.run_polling(bot)


@cli.command("webhook")
@click.option("-r", "--reset-webhook", is_flag=True, default=False)
def run_webhook(reset_webhook: bool) -> None:
    app: web.Application = web.Application()
    dp: Dispatcher = create_dispatcher()
    settings: Settings = dp["settings"]

    bot: Bot = create_bot(settings=settings)
    dp.startup.register(webhook_startup)
    dp.shutdown.register(webhook_shutdown)

    server.SimpleRequestHandler(
        dispatcher=dp, bot=bot, secret_token=settings.webhook.secret_token
    ).register(app, path=settings.webhook.path)
    server.setup_application(app, dp, bot=bot, reset_webhook=reset_webhook)

    return web.run_app(
        app=app,
        host=settings.webhook.host,
        port=settings.webhook.port,
        print=MultilineLogger(),
    )


if __name__ == "__main__":
    cli()
