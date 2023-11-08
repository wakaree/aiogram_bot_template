from typing import Any, Awaitable, Callable, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

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
        if user:
            repository: Repository = data["repository"]
            db_user: Optional[DBUser] = await repository.get_user(pk=user.id)
            if not db_user:
                db_user = await repository.create_user(user=user)
            data["user"] = db_user
        return await handler(event, data)
