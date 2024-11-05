from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import Router, flags
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext

from ...keyboards.callback_data.menu import CDPing
from ...keyboards.menu import ping_keyboard

if TYPE_CHECKING:
    from ....models.sql import User

router: Final[Router] = Router(name=__name__)


@router.message(CommandStart())
async def greeting(message: Message, i18n: I18nContext, user: User) -> Any:
    return message.answer(
        text=i18n.messages.hello(name=user.mention, _path="menu.ftl"),
        reply_markup=ping_keyboard(i18n=i18n),
    )


@router.callback_query(CDPing.filter())
@flags.callback_answer(disabled=True)
async def answer_pong(query: CallbackQuery, i18n: I18nContext) -> Any:
    return query.answer(text=i18n.messages.pong(_path="menu.ftl"))
