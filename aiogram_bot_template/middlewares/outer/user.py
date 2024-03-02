from __future__ import annotations

from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional, cast

from aiogram import BaseMiddleware
from aiogram.types import Chat, TelegramObject, User
from aiogram_i18n import I18nMiddleware

from ...services.database import DBUser
from ...utils.loggers import database as logger

if TYPE_CHECKING:
    from ...services.database import Repository, UoW


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Optional[Any]:
        aiogram_user: Optional[User] = data.get("event_from_user")
        chat: Optional[Chat] = data.get("event_chat")
        if aiogram_user is None or chat is None or aiogram_user.is_bot:
            # Prevents the bot itself from being added to the database
            # when accepting chat_join_request and receiving chat_member.
            return await handler(event, data)

        repository: Repository = data["repository"]
        user: Optional[DBUser] = await repository.users.get(user_id=aiogram_user.id)
        if user is None:
            i18n: I18nMiddleware = data["i18n_middleware"]
            uow: UoW = data["uow"]
            user = DBUser.from_aiogram(
                user=aiogram_user,
                locale=(
                    aiogram_user.language_code
                    if aiogram_user.language_code in i18n.core.available_locales
                    else cast(str, i18n.core.default_locale)
                ),
                chat=chat,
            )
            await uow.commit(user)
            logger.info("New user in database: %s (%d)", aiogram_user.full_name, aiogram_user.id)

        data["user"] = user
        return await handler(event, data)
