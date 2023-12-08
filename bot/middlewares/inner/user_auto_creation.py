from __future__ import annotations

from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional

from aiogram.enums import UpdateType
from aiogram.types import TelegramObject, User

from utils.loggers import database

from ..event_typed import EventTypedMiddleware

if TYPE_CHECKING:
    from bot.models import DBUser
    from bot.services.database import Repository


class UserAutoCreationMiddleware(EventTypedMiddleware):
    __event_types__ = [UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY, UpdateType.MY_CHAT_MEMBER]

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Optional[Any]:
        aiogram_user: Optional[User] = data.get("event_from_user")
        if aiogram_user is None:
            return await handler(event, data)
        if "user" not in data:
            repository: Repository = data["repository"]
            user: DBUser = await repository.user.create(user=aiogram_user, chat=data["event_chat"])
            database.info("New user in database: %s (%d)", user.name, user.id)
            data["user"] = user
        return await handler(event, data)
