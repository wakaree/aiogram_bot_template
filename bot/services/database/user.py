from aiogram.enums import ChatType
from aiogram.types import Chat, User
from sqlalchemy.ext.asyncio import AsyncSession

from bot.enums import Locale
from bot.models import DBUser

from .base import BaseRepository


class UserRepository(BaseRepository[DBUser]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, entity=DBUser)

    async def create(self, user: User, chat: Chat) -> DBUser:
        db_user: DBUser = DBUser(
            id=user.id,
            name=user.full_name,
            locale=Locale.resolve(user.language_code),
            notifications=chat.type == ChatType.PRIVATE,
        )
        await self.save(db_user)
        return db_user
