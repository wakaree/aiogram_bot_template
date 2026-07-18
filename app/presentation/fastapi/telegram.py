import asyncio
import secrets
from typing import Annotated, Any, Optional

from aiogram import Bot, Dispatcher
from aiogram.methods import TelegramMethod
from aiogram.types import Update
from fastapi import APIRouter, Body, Header, HTTPException, status


class TelegramRequestHandler:
    dispatcher: Dispatcher
    bot: Bot
    secret_token: Optional[str]
    _feed_update_tasks: set[asyncio.Task[Any]]

    def __init__(
        self,
        dispatcher: Dispatcher,
        bot: Bot,
        path: str,
        secret_token: Optional[str] = None,
    ) -> None:
        """
        Base handler that helps to handle incoming request from aiohttp
        and propagate it to the Dispatcher
        """
        self.dispatcher = dispatcher
        self.bot = bot
        self.secret_token = secret_token
        self.router: APIRouter = APIRouter(
            on_startup=(self.startup,),
            on_shutdown=(self.shutdown,),
            include_in_schema=False,
        )
        self.router.add_api_route(path=path, endpoint=self.handle, methods=["POST"])
        self._feed_update_tasks = set()

    async def startup(self) -> None:
        await self.dispatcher.emit_startup(
            dispatcher=self.dispatcher,
            bot=self.bot,
            **self.dispatcher.workflow_data,
        )

    async def shutdown(self) -> None:
        if self.dispatcher.get("shutdown_completed"):
            return
        await self.dispatcher.emit_shutdown(
            dispatcher=self.dispatcher,
            bot=self.bot,
            **self.dispatcher.workflow_data,
        )
        self.dispatcher["shutdown_completed"] = True

    async def close(self) -> None:
        await self.bot.session.close()

    def verify_secret(self, telegram_secret_token: str) -> bool:
        if self.secret_token:
            return secrets.compare_digest(telegram_secret_token, self.secret_token)
        return True

    async def _feed_update(self, update: Update) -> None:
        result = await self.dispatcher.feed_update(
            bot=self.bot,
            update=update,
            dispatcher=self.dispatcher,
        )
        if isinstance(result, TelegramMethod):
            await self.dispatcher.silent_call_request(bot=self.bot, result=result)

    async def _handle_request_background(self, update: Update) -> None:
        feed_update_task: asyncio.Task[Any] = asyncio.create_task(self._feed_update(update=update))
        self._feed_update_tasks.add(feed_update_task)
        feed_update_task.add_done_callback(self._feed_update_tasks.discard)

    async def handle(
        self,
        update: Annotated[Update, Body()],
        x_telegram_bot_api_secret_token: Annotated[str, Header()],
    ) -> None:
        if not self.verify_secret(x_telegram_bot_api_secret_token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid secret token",
            )
        await self._handle_request_background(update=update)
