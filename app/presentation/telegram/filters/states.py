from typing import Final

from aiogram.filters import Filter, StateFilter

NoneState: Final[Filter] = StateFilter(None)
AnyState: Final[Filter] = ~NoneState
