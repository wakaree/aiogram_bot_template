from typing import Any, Awaitable, Callable, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from bot.enums import Locale
from bot.models import DBUser
from bot.services import Repository
from utils.loggers import database


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
            db_user = await repository.get_user(pk=user.id)
            if not db_user:
                db_user = DBUser(
                    id=user.id, name=user.full_name, locale=Locale.resolve(user.language_code)
                )
                await repository.save(db_user)
                database.info("New user in database: %s (%d)", user.full_name, user.id)
            data["user"] = db_user
        return await handler(event, data)
