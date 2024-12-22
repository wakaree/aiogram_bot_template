from aiogram.filters.callback_data import CallbackData


class CDPing(CallbackData, prefix="ping"):
    pass
