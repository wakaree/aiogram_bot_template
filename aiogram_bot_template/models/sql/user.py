from aiogram import html
from aiogram.utils.link import create_tg_link
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, Int64
from .mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[Int64] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[Int64] = mapped_column(nullable=False, unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    locale: Mapped[str] = mapped_column(String(length=2), nullable=False)
    bot_blocked: Mapped[bool] = mapped_column(default=False, nullable=False)

    @property
    def url(self) -> str:
        return create_tg_link("user", id=self.telegram_id)

    @property
    def mention(self) -> str:
        return html.link(value=self.name, link=self.url)
