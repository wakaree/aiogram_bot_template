from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from aiogram.types import InlineKeyboardMarkup


class RenderMode(str, Enum):
    # helper.answer(...) — редактирует текущее сообщение, если можно, иначе шлёт новое
    ANSWER = "answer"
    # helper.send_new_message(...) — гарантированно новое сообщение
    NEW = "new"
    # ничего не рендерить (например, обработали апдейт без ответа пользователю)
    NONE = "none"


@dataclass()
class View:
    text: str | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    mode: RenderMode = RenderMode.ANSWER

    edit: bool = True
    reply: bool = False
    delete: bool = False
    force_edit: bool = False
    message_id: int | None = None
    chat_id: int | None = None
    kwargs: dict[str, Any] | None = None
