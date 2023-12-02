from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from aiogram.types import User
from aiogram_i18n.managers import BaseManager

if TYPE_CHECKING:
    from bot.middlewares import Commit
    from bot.models import DBUser


class UserManager(BaseManager):
    async def get_locale(
        self, event_from_user: Optional[User] = None, user: Optional[DBUser] = None
    ) -> str:
        if user:
            return user.locale
        if event_from_user:
            return event_from_user.language_code or self.default_locale
        return self.default_locale

    async def set_locale(self, locale: str, user: DBUser, commit: Commit) -> None:
        user.locale = locale
        commit.confirm()
