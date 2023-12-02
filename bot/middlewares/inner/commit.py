from __future__ import annotations

from typing import TYPE_CHECKING, Any, Awaitable, Callable

from aiogram.dispatcher.flags import get_flag
from aiogram.enums import UpdateType
from aiogram.types import TelegramObject

from ..event_typed import EventTypedMiddleware

if TYPE_CHECKING:
    from bot.models import DBUser
    from bot.services.database import Repository


class Commit:
    confirmed: bool

    __slots__ = ("confirmed",)

    def __init__(self, confirmed: bool) -> None:
        self.confirmed = confirmed

    def confirm(self) -> None:
        self.confirmed = True

    def reject(self) -> None:
        self.confirmed = False


class CommitMiddleware(EventTypedMiddleware):
    __event_types__ = [UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY, UpdateType.MY_CHAT_MEMBER]

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        repository: Repository = data["repository"]
        user: DBUser = data["user"]
        commit: Commit = Commit(confirmed=get_flag(data, "do_commit", default=False))

        try:
            data["commit"] = commit
            return await handler(event, data)
        finally:
            if commit.confirmed:
                await repository.user.save(model=user)
