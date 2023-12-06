from typing import Any, Final

from aiogram import F, Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.methods import TelegramMethod
from aiogram.types import ErrorEvent
from aiogram_i18n import I18nContext

from bot.exceptions import BotError

router: Final[Router] = Router(name=__name__)


@router.error(ExceptionTypeFilter(BotError), F.update.message)
async def handle_some_error(error: ErrorEvent, i18n: I18nContext) -> TelegramMethod[Any]:
    return error.update.message.answer(text=i18n.messages.something_went_wrong())
