from __future__ import annotations

from typing import Optional, cast

from aiogram.types import User as AiogramUser
from aiogram_i18n.managers import BaseManager
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from app.application.ports.repositories.users import UsersGateway
from app.domain.user import User


class UserManager(BaseManager):
    @inject
    async def get_locale(
        self,
        user: FromDishka[User],
        event_from_user: Optional[AiogramUser] = None,
    ) -> str:
        locale: Optional[str] = None
        if user is not None:
            locale = user.language
        elif event_from_user is not None and event_from_user.language_code is not None:
            locale = event_from_user.language_code
        return locale or cast(str, self.default_locale)

    @inject
    async def set_locale(
        self,
        locale: str,
        user: FromDishka[User],
        users_gateway: FromDishka[UsersGateway],
    ) -> None:
        user.language = locale
        await users_gateway.save(user)
