from typing import Any, Final

from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import JOIN_TRANSITION, LEAVE_TRANSITION, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated
from dishka import FromDishka

from app.presentation.telegram.flows.extra.pm import PMFlow

router: Final[Router] = Router(name=__name__)
router.my_chat_member.filter(F.chat.type == ChatType.PRIVATE)


@router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def bot_unblocked(_: ChatMemberUpdated, flow: FromDishka[PMFlow]) -> Any:
    await flow.mark_unblocked()


@router.my_chat_member(ChatMemberUpdatedFilter(LEAVE_TRANSITION))
async def bot_blocked(_: ChatMemberUpdated, flow: FromDishka[PMFlow]) -> Any:
    await flow.mark_blocked()
