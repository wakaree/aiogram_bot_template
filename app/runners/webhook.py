from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from aiogram import Dispatcher
from dishka import AsyncContainer
from fastapi import FastAPI

from app.infrastructure.telegram.lifespan import LifespanService


@asynccontextmanager
async def webhook_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    container: AsyncContainer = app.state.dishka_container
    dispatcher: Dispatcher = app.state.dispatcher
    lifespan: LifespanService = await container.get(LifespanService)

    await lifespan.setup_webhooks(dispatcher=dispatcher)
    await lifespan.setup_commands()
    yield
    await lifespan.reset_webhooks()
    await container.close()
