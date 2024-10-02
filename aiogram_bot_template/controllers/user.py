from typing import Any, cast

from aiogram.types import User as AiogramUser
from aiogram_i18n.cores import BaseCore

from ..models.sql import User
from ..services.sql import UoW


async def create_user(aiogram_user: AiogramUser, uow: UoW, i18n_core: BaseCore[Any]) -> User:
    user: User = User(
        telegram_id=aiogram_user.id,
        name=aiogram_user.full_name,
        locale=(
            aiogram_user.language_code
            if aiogram_user.language_code in i18n_core.locales
            else cast(str, i18n_core.default_locale)
        ),
    )
    await uow.commit(user)
    return user


async def set_bot_blocked(user: User, uow: UoW, bot_blocked: bool) -> None:
    user.bot_blocked = bot_blocked
    await uow.commit(user)
