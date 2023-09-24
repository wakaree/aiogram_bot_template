from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup


class SGForm(StatesGroup):
    name = State()
    age = State()


NoneState = StateFilter(None)
AnyState = ~NoneState
