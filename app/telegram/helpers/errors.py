from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError


def silent_bot_request() -> suppress:
    return suppress(TelegramBadRequest, TelegramForbiddenError)
