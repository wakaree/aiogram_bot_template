from typing import Any, Final

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.methods import TelegramMethod
from aiogram.types import Message
from aiogram_i18n import I18nContext

from bot.models import DBUser

router: Final[Router] = Router(name=__name__)


@router.message(CommandStart())
async def start_command(message: Message, i18n: I18nContext, user: DBUser) -> TelegramMethod[Any]:
    return message.answer(text=i18n.messages.start(name=user.mention))
