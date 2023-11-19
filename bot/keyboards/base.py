from typing import Optional

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def common_keyboard(
    *texts: str,
    is_persistent: Optional[bool] = None,
    resize_keyboard: bool = True,
    one_time_keyboard: Optional[bool] = None,
    input_field_placeholder: Optional[str] = None,
    selective: Optional[bool] = None,
    row_width: int = 2
) -> ReplyKeyboardMarkup:
    """
    Common reply keyboards build helper.
    """
    builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    builder.row(*[KeyboardButton(text=text) for text in texts], width=row_width)
    return builder.as_markup(
        is_persistent=is_persistent,
        resize_keyboard=resize_keyboard,
        one_time_keyboard=one_time_keyboard,
        input_field_placeholder=input_field_placeholder,
        selective=selective,
    )
