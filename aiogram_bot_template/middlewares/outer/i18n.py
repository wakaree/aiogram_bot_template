from __future__ import annotations

from typing import TYPE_CHECKING, Optional, cast

from aiogram.types import User
from aiogram_i18n.managers import BaseManager

if TYPE_CHECKING:
    from ...services.database import DBUser, UoW


class UserManager(BaseManager):
    async def get_locale(
        self, event_from_user: Optional[User] = None, user: Optional[DBUser] = None
    ) -> str:
        if user:
            return user.locale
        if event_from_user and event_from_user.language_code is not None:
            return event_from_user.language_code
        return cast(str, self.default_locale)

    async def set_locale(self, locale: str, user: DBUser, uow: UoW) -> None:
        user.locale = locale
        await uow.commit(user)
