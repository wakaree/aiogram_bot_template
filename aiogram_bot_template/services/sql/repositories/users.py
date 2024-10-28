from typing import Optional

from .base import BaseRepository
from ....models.sql import User


class UsersRepository(BaseRepository):
    async def get(self, user_id: int) -> Optional[User]:
        return await self._get(User, User.id == user_id)

    async def by_tg_id(self, telegram_id: int) -> Optional[User]:
        return await self._get(User, User.telegram_id == telegram_id)
