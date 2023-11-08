from typing import Any, Final

from aiogram import F, Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.methods import TelegramMethod
from aiogram.types import ErrorEvent
from aiogram_i18n import I18nContext as L10n

from bot.exceptions import BotError

router: Final[Router] = Router(name=__name__)


@router.error(ExceptionTypeFilter(BotError), F.update.message)
async def handle_some_error(error: ErrorEvent, l10n: L10n) -> TelegramMethod[Any]:
    return error.update.message.answer(text=l10n.messages.something_went_wrong())
