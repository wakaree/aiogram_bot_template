from typing import Optional, Self

from aiogram.fsm.context import FSMContext
from pydantic import ValidationError

from app.errors.bot import UnknownMessageError
from app.models.base import PydanticModel


class StateModel(PydanticModel):
    @classmethod
    async def from_state(cls, state: FSMContext) -> Self:
        try:
            # noinspection PyArgumentList
            return cls(**await state.get_data())
        except ValidationError as error:
            raise UnknownMessageError() from error

    @classmethod
    async def optional_from_state(cls, state: FSMContext) -> Optional[Self]:
        try:
            # noinspection PyArgumentList
            return cls(**await state.get_data())
        except ValidationError:
            return None

    async def update_state(self, state: FSMContext) -> None:
        await state.update_data(self.model_dump())
