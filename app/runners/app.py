from __future__ import annotations

import asyncio
import signal
from functools import partial
from typing import Any

import uvicorn
from aiogram import Bot, Dispatcher
from dishka import AsyncContainer
from fastapi import FastAPI
from uvicorn import server

from app.application.models.config import AppConfig
from app.presentation.fastapi.telegram import TelegramRequestHandler
from app.providers.telegram.fastapi import setup_fastapi
from app.runners.lifespan import emit_aiogram_shutdown
from app.runners.polling import polling_lifespan
from app.runners.webhook import webhook_lifespan


# noinspection PyProtectedMember
def handle_sigterm(*_: Any, app: FastAPI) -> None:
    if app.state.is_polling:
        app.state.dispatcher._signal_stop_polling(sig=signal.SIGTERM)
        app.state.shutdown_completed = True
    else:
        asyncio.create_task(emit_aiogram_shutdown(app=app))


async def run_app(app: FastAPI, dispatcher: Dispatcher, container: AsyncContainer) -> None:
    setup_fastapi(app=app, dispatcher=dispatcher, container=container)
    config: AppConfig = await container.get(AppConfig)
    server.HANDLED_SIGNALS = (signal.SIGINT,)  # type: ignore
    signal.signal(signal.SIGTERM, partial(handle_sigterm, app=app))
    uvicorn_config = uvicorn.Config(
        app=app,
        host=config.server.host,
        port=config.server.port,
        access_log=False,
    )
    uvicorn_server = uvicorn.Server(config=uvicorn_config)
    return await uvicorn_server.serve()


async def run_polling(dispatcher: Dispatcher, container: AsyncContainer) -> None:
    app: FastAPI = FastAPI(lifespan=polling_lifespan)
    app.state.is_polling = True
    return await run_app(app=app, dispatcher=dispatcher, container=container)


async def run_webhook(dispatcher: Dispatcher, container: AsyncContainer) -> None:
    app: FastAPI = FastAPI(lifespan=webhook_lifespan)
    app.state.is_polling = False
    config: AppConfig = await container.get(AppConfig)
    bot: Bot = await container.get(Bot)
    handler: TelegramRequestHandler = TelegramRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
        path=config.telegram.webhook_path,
        secret_token=config.telegram.webhook_secret.get_secret_value(),
    )
    app.state.tg_webhook_handler = handler
    app.include_router(handler.router)
    dispatcher.workflow_data.update(app=app)
    return await run_app(app=app, dispatcher=dispatcher, container=container)
