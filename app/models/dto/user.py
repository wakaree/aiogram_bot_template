from datetime import datetime
from typing import Optional

from aiogram import html
from aiogram.utils.link import create_tg_link

from app.models.base import PydanticModel


class UserDto(PydanticModel):
    id: int
    telegram_id: int
    name: str
    language: str
    language_code: Optional[str] = None
    bot_blocked: bool = False
    blocked_at: Optional[datetime] = None

    @property
    def url(self) -> str:
        return create_tg_link("user", id=self.telegram_id)

    @property
    def mention(self) -> str:
        return html.link(value=self.name, link=self.url)
