from __future__ import annotations

from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional

from aiogram.types import TelegramObject
from aiogram.types import User as AiogramUser
from aiogram_i18n import I18nMiddleware

from app.services.crud.user import UserService
from app.telegram.middlewares.event_typed import EventTypedMiddleware
from app.utils.logging import database as logger

if TYPE_CHECKING:
    from app.models.dto.user import UserDto


class UserMiddleware(EventTypedMiddleware):
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

        user_service: UserService = data["user_service"]
        user: Optional[UserDto] = await user_service.get(user_id=aiogram_user.id)
        if user is None:
            i18n: I18nMiddleware = data["i18n_middleware"]
            user = await user_service.create(aiogram_user=aiogram_user, i18n_core=i18n.core)
            logger.info(
                "New user in database: %s (%d)",
                aiogram_user.full_name,
                aiogram_user.id,
            )

        data["user"] = user
        return await handler(event, data)
