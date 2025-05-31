from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext

from app.telegram.keyboards.callback_data.menu import CDMenu


def back_keyboard(i18n: I18nContext, data: CallbackData = CDMenu()) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.button(text=i18n.buttons.back(), callback_data=data)
    return builder.as_markup()
