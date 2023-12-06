from __future__ import annotations

from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

if TYPE_CHECKING:
    from bot.models import DBUser
    from bot.services.database import Repository


class UserAccessMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Optional[Any]:
        aiogram_user: Optional[User] = data.get("event_from_user")
        if aiogram_user is None:
            return await handler(event, data)
        repository: Repository = data["repository"]
        user: Optional[DBUser] = await repository.user.get(pk=aiogram_user.id)
        if user:
            data["user"] = user
        return await handler(event, data)
