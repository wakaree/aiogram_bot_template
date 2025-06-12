from __future__ import annotations

from typing import TYPE_CHECKING, Optional, cast

from aiogram.types import User as AiogramUser
from aiogram_i18n.managers import BaseManager

from app.services.crud import UserService

if TYPE_CHECKING:
    from app.models.dto.user import UserDto


class UserManager(BaseManager):
    async def get_locale(
        self,
        event_from_user: Optional[AiogramUser] = None,
        user: Optional[UserDto] = None,
    ) -> str:
        locale: Optional[str] = None
        if user is not None:
            locale = user.language
        elif event_from_user is not None and event_from_user.language_code is not None:
            locale = event_from_user.language_code
        return locale or cast(str, self.default_locale)

    async def set_locale(self, locale: str, user: UserDto, user_service: UserService) -> None:
        await user_service.update(user=user, language=locale)
