from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Dispatcher
from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject

from bot.models import DBUser
from bot.services import Repository


class Commit:
    confirmed: bool

    def __init__(self, confirmed: bool) -> None:
        self.confirmed = confirmed

    def confirm(self) -> None:
        self.confirmed = True

    def reject(self) -> None:
        self.confirmed = False

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> Commit:
        return cls(confirmed=get_flag(data, "do_commit", default=False))


class CommitMiddleware(BaseMiddleware):
    def setup(self, dp: Dispatcher) -> None:
        dp.message.middleware(self)
        dp.callback_query.middleware(self)
        dp.my_chat_member.middleware(self)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        repository: Repository = data["repository"]
        user: DBUser = data["user"]
        commit = data["commit"] = Commit.from_data(data)

        try:
            return await handler(event, data)
        finally:
            if commit.confirmed:
                await repository.save(user)
