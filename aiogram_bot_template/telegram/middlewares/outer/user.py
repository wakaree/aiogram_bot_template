from __future__ import annotations

from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.types import User as AiogramUser
from aiogram_i18n import I18nMiddleware

from ....controllers.user import create_user
from ....utils.logging import database as logger

if TYPE_CHECKING:
    from ....models.sql import User
    from ....services.sql import Repository, UoW


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Optional[Any]:
        aiogram_user: Optional[AiogramUser] = data.get("event_from_user")
        if aiogram_user is None or aiogram_user.is_bot:
            # Prevents the bot itself from being added to the database
            # when accepting chat_join_request and receiving chat_member updates.
            return await handler(event, data)

        repository: Repository = data["repository"]
        user: Optional[User] = await repository.users.by_tg_id(telegram_id=aiogram_user.id)
        if user is None:
            i18n: I18nMiddleware = data["i18n_middleware"]
            uow: UoW = data["uow"]
            user = await create_user(
                aiogram_user=aiogram_user,
                uow=uow,
                i18n_core=i18n.core,
            )
            logger.info(
                "New user in database: %s (%d)",
                aiogram_user.full_name,
                aiogram_user.id,
            )

        data["user"] = user
        return await handler(event, data)
