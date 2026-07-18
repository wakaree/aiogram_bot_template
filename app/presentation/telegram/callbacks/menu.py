from aiogram.filters.callback_data import CallbackData


class CDDeposit(CallbackData, prefix="deposit"):
    pass


class CDMenu(CallbackData, prefix="menu"):
    pass
