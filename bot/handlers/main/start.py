from typing import Any, Final

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.methods import TelegramMethod
from aiogram.types import Message
from aiogram_i18n import I18nContext as L10n

from bot.models import DBUser

router: Final[Router] = Router(name=__name__)


@router.message(CommandStart())
async def start_command(message: Message, l10n: L10n, user: DBUser) -> TelegramMethod[Any]:
    return message.answer(text=l10n.messages.start(name=user.mention))
