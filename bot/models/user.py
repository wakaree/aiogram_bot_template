from __future__ import annotations

from aiogram import html
from aiogram.utils.link import create_tg_link
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..enums import Locale
from .base import Base, Int64, TimestampMixin


class DBUser(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[Int64] = mapped_column(primary_key=True)
    name: Mapped[str]
    locale: Mapped[str] = mapped_column(String(length=2), default=Locale.DEFAULT)
    notifications: Mapped[bool] = mapped_column(default=False)

    @property
    def url(self) -> str:
        return create_tg_link("user", id=self.id)

    @property
    def mention(self) -> str:
        return html.link(value=self.name, link=self.url)
