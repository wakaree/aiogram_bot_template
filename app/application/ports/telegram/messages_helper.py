from __future__ import annotations

from datetime import datetime
from typing import Any, Optional, Protocol

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from app.utils.custom_types import AnyKeyboard


class MessageHelper(Protocol):
    update: Optional[Message | CallbackQuery]
    chat_id: Optional[int]
    message_id: Optional[int]
    bot: Bot
    fsm_context: Optional[FSMContext]
    last_updated: datetime

    @property
    def fsm(self) -> FSMContext: ...

    def copy(
        self,
        *,
        update: Optional[Message | CallbackQuery] = None,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
    ) -> MessageHelper: ...

    def resolve_message_id(
        self,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
    ) -> tuple[int, Optional[int], bool]: ...

    def get_chat_id(self) -> int: ...

    def find_message_id(self) -> Optional[int]: ...

    async def get_message_id(self, from_state: bool = True) -> Optional[int]: ...

    async def delete(
        self,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
    ) -> bool: ...

    async def delete_many(
        self,
        chat_id: Optional[int] = None,
        message_ids: Optional[list[int]] = None,
    ) -> None: ...

    async def send_new_message(
        self,
        *,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        text: str,
        reply_markup: Optional[AnyKeyboard] = None,
        delete: bool = True,
        **kwargs: Any,
    ) -> Message: ...

    async def answer(
        self,
        *,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        text: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        edit: bool = True,
        reply: bool = False,
        delete: bool = False,
        force_edit: bool = False,
        **kwargs: Any,
    ) -> bool | Message: ...

    async def answer_current_message(
        self,
        *,
        message_id: Optional[int] = None,
        text: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        fsm_data: Optional[dict[str, Any]] = None,
        delete_user_message: bool = True,
        clear_messages: bool = True,
        send_new: bool = False,
        **kwargs: Any,
    ) -> tuple[Message | bool, dict[str, Any]]: ...
