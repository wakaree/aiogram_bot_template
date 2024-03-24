from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import JOIN_TRANSITION, LEAVE_TRANSITION, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated

if TYPE_CHECKING:
    from ....services.database import DBUser, UoW

router: Final[Router] = Router(name=__name__)
router.my_chat_member.filter(F.chat.type == ChatType.PRIVATE)


@router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def enable_notifications(_: ChatMemberUpdated, user: DBUser, uow: UoW) -> Any:
    user.enable_notifications()
    await uow.commit(user)


@router.my_chat_member(ChatMemberUpdatedFilter(LEAVE_TRANSITION))
async def disable_notifications(_: ChatMemberUpdated, user: DBUser, uow: UoW) -> Any:
    user.disable_notifications()
    await uow.commit(user)
