from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from .user import UserRepository


class Repository(BaseRepository):
    """
    The general repository.
    """

    user: UserRepository

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)
        self.user = UserRepository(session=session)
