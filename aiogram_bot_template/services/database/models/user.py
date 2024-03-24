from typing import Self

from aiogram import html
from aiogram.enums import ChatType
from aiogram.types import Chat, User
from aiogram.utils.link import create_tg_link
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, Int64, TimestampMixin


class DBUser(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[Int64] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    locale: Mapped[str] = mapped_column(String(length=2), nullable=False)
    notifications: Mapped[bool] = mapped_column(default=False, nullable=False)

    @property
    def url(self) -> str:
        return create_tg_link("user", id=self.id)

    @property
    def mention(self) -> str:
        return html.link(value=self.name, link=self.url)

    @classmethod
    def from_aiogram(cls, user: User, locale: str, chat: Chat) -> Self:
        return cls(
            id=user.id,
            name=user.full_name,
            locale=locale,
            notifications=chat.type == ChatType.PRIVATE,
        )

    def enable_notifications(self) -> None:
        self.notifications = True  # noqa

    def disable_notifications(self) -> None:
        self.notifications = False  # noqa
