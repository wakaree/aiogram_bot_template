from datetime import datetime
from typing import Optional

from aiogram import html
from aiogram.utils.link import create_tg_link

from app.models.base import ActiveRecordModel


class UserDto(ActiveRecordModel):
    id: int
    name: str
    language: str
    language_code: Optional[str] = None
    bot_blocked: bool = False
    blocked_at: Optional[datetime] = None

    @property
    def url(self) -> str:
        return create_tg_link("user", id=self.id)

    @property
    def mention(self) -> str:
        return html.link(value=self.name, link=self.url)
