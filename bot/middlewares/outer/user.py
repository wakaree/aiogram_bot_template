from __future__ import annotations

from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from utils.loggers import database

if TYPE_CHECKING:
    from bot.models import DBUser
    from bot.services import Repository


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Optional[Any]:
        user: Optional[User] = data.get("event_from_user")
        if user is not None:
            repository: Repository = data["repository"]
            db_user: Optional[DBUser] = await repository.get_user(pk=user.id)
            if db_user is None:
                db_user = await repository.create_user(user=user)
                database.info("New user in database: %s (%d)", user.full_name, user.id)
            data["user"] = db_user
        return await handler(event, data)
