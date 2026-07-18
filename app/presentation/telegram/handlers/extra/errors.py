from typing import Any, Final

from aiogram import F, Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from dishka import FromDishka

from app.application.errors.base import AppError
from app.presentation.telegram.flows.extra.errors import ExtraErrorsFlow

router: Final[Router] = Router(name=__name__)


@router.error(ExceptionTypeFilter(AppError), F.update.message)
async def handle_some_error(_: ErrorEvent, flow: FromDishka[ExtraErrorsFlow]) -> Any:
    await flow.answer_something_went_wrong()
