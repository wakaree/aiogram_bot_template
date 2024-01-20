from typing import Optional, cast

from aiogram.enums import ChatType
from aiogram.types import Chat, User
from sqlalchemy import select

from ..models import DBUser
from .base import BaseRepository


class UserRepository(BaseRepository):
    async def get(self, user_id: int) -> Optional[DBUser]:
        return cast(
            Optional[DBUser],
            await self._session.scalar(select(DBUser).where(DBUser.id == user_id)),
        )

    async def create_from_telegram(self, user: User, locale: str, chat: Chat) -> DBUser:
        db_user: DBUser = DBUser(
            id=user.id,
            name=user.full_name,
            locale=locale,
            notifications=chat.type == ChatType.PRIVATE,
        )

        await self.commit(db_user)
        return db_user
