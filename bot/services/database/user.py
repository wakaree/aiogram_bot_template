from aiogram.types import User
from sqlalchemy.ext.asyncio import AsyncSession

from bot.enums import Locale
from bot.models import DBUser

from .base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, entity=DBUser)

    async def create(self, user: User) -> DBUser:
        db_user: DBUser = DBUser(
            id=user.id, name=user.full_name, locale=Locale.resolve(user.language_code)
        )
        await self.save(db_user)
        return db_user
