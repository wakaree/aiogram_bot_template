from __future__ import annotations

from datetime import datetime

from aiogram import html
from aiogram.utils.link import create_tg_link
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from ..enums import Locale
from .base import Base, Int64


class DBUser(Base):
    __tablename__ = "users"

    id: Mapped[Int64] = mapped_column(primary_key=True)
    name: Mapped[str]
    locale: Mapped[str] = mapped_column(String(length=8), default=Locale.DEFAULT)
    register_date: Mapped[datetime] = mapped_column(server_default=func.now())
    notifications: Mapped[bool] = mapped_column(default=False)

    @property
    def url(self) -> str:
        return create_tg_link("user", id=self.id)

    @property
    def mention(self) -> str:
        return html.link(self.name, self.url)
