from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram_i18n.managers import BaseManager

if TYPE_CHECKING:
    from bot.middlewares import Commit
    from bot.models import DBUser


class UserManager(BaseManager):
    async def get_locale(self, user: DBUser) -> str:
        return user.locale

    async def set_locale(self, locale: str, user: DBUser, commit: Commit) -> None:
        user.locale = locale
        commit.confirm()
