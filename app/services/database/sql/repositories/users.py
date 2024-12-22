from typing import Any, Optional

from app.models.sql import User

from .base import BaseRepository


class UsersRepository(BaseRepository):
    async def get(self, user_id: int) -> Optional[User]:
        return await self._get(User, User.id == user_id)

    async def by_tg_id(self, telegram_id: int) -> Optional[User]:
        return await self._get(User, User.telegram_id == telegram_id)

    async def update(self, user_id: int, **kwargs: Any) -> Optional[User]:
        return await self._update(
            model=User,
            conditions=[User.id == user_id],
            load_result=False,
            **kwargs,
        )

    async def delete(self, user_id: int) -> bool:
        return await self._delete(User, User.id == user_id)
