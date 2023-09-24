from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


class CommonKeyboard(ReplyKeyboardMarkup):
    def __init__(self, *texts: str, row_width: int = 2) -> None:
        builder = ReplyKeyboardBuilder()
        builder.row(*[KeyboardButton(text=text) for text in texts], width=row_width)
        super().__init__(keyboard=builder.export(), resize_keyboard=True)


class CommonInlineKeyboard(InlineKeyboardMarkup):
    def __init__(self, *buttons: InlineKeyboardButton, row_width: int = 2) -> None:
        builder = InlineKeyboardBuilder()
        builder.row(*buttons, width=row_width)
        super().__init__(inline_keyboard=builder.export())
