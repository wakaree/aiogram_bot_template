from typing import Final

from aiogram import Router, flags
from aiogram.filters import JOIN_TRANSITION, LEAVE_TRANSITION, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated

from bot.filters import PRIVATE_ONLY
from bot.models import DBUser

router: Final[Router] = Router(name=__name__)
router.my_chat_member.filter(PRIVATE_ONLY)


@router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
@flags.do_commit(True)
async def enable_notifications(_: ChatMemberUpdated, user: DBUser) -> None:
    user.notifications = True


@router.my_chat_member(ChatMemberUpdatedFilter(LEAVE_TRANSITION))
@flags.do_commit(True)
async def disable_notifications(_: ChatMemberUpdated, user: DBUser) -> None:
    user.notifications = False
