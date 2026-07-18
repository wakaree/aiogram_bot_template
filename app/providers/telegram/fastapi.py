from aiogram import Dispatcher
from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.presentation.fastapi import healthcheck


def setup_fastapi(app: FastAPI, dispatcher: Dispatcher, container: AsyncContainer) -> FastAPI:
    app.include_router(healthcheck.router)
    for key, value in dispatcher.workflow_data.items():
        setattr(app.state, key, value)
    app.state.dispatcher = dispatcher
    app.state.shutdown_completed = False
    setup_dishka(container=container, app=app)
    return app
