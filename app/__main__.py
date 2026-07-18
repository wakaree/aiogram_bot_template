from contextlib import suppress

from aiogram import Dispatcher
from dishka import AsyncContainer

from app.application.models.config import AppConfig
from app.providers.container import create_container
from app.providers.telegram.dispatcher import create_dispatcher
from app.runners.app import run_polling, run_webhook
from app.utils.logging import setup_logger


async def main() -> None:
    container: AsyncContainer = create_container()
    config: AppConfig = await container.get(AppConfig)
    setup_logger()
    dispatcher: Dispatcher = await create_dispatcher(container=container)
    if config.telegram.use_webhook:
        return await run_webhook(dispatcher=dispatcher, container=container)
    return await run_polling(dispatcher=dispatcher, container=container)


if __name__ == "__main__":
    import asyncio

    with suppress(KeyboardInterrupt):
        asyncio.run(main())
