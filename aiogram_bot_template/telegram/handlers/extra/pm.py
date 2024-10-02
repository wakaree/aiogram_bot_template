from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import JOIN_TRANSITION, LEAVE_TRANSITION, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated

from ....controllers.user import set_bot_blocked

if TYPE_CHECKING:
    from ....models.sql import User
    from ....services.sql import UoW

router: Final[Router] = Router(name=__name__)
router.my_chat_member.filter(F.chat.type == ChatType.PRIVATE)


@router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def bot_unblocked(_: ChatMemberUpdated, user: User, uow: UoW) -> Any:
    await set_bot_blocked(user=user, uow=uow, bot_blocked=False)


@router.my_chat_member(ChatMemberUpdatedFilter(LEAVE_TRANSITION))
async def bot_blocked(_: ChatMemberUpdated, user: User, uow: UoW) -> Any:
    await set_bot_blocked(user=user, uow=uow, bot_blocked=True)
