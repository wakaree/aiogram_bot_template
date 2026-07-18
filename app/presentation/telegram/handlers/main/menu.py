from typing import Any, Final

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import TelegramObject
from dishka import FromDishka

from app.presentation.telegram.callbacks.menu import CDDeposit, CDMenu
from app.presentation.telegram.flows.common.menu import CommonMenuFlow

router: Final[Router] = Router(name=__name__)


@router.message(CommandStart())
@router.callback_query(CDMenu.filter())
async def greeting(_: TelegramObject, flow: FromDishka[CommonMenuFlow]) -> Any:
    return await flow.greeting()


@router.callback_query(CDDeposit.filter())
async def answer_deposit(_: TelegramObject, flow: FromDishka[CommonMenuFlow]) -> Any:
    return await flow.answer_deposit()
