from __future__ import annotations

from typing import Any, Final, TYPE_CHECKING

from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import JOIN_TRANSITION, LEAVE_TRANSITION, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated

from app.utils.time import datetime_now

if TYPE_CHECKING:
    from app.models.dto.user import UserDto
    from app.services.crud import UserService

router: Final[Router] = Router(name=__name__)
router.my_chat_member.filter(F.chat.type == ChatType.PRIVATE)


@router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def bot_unblocked(_: ChatMemberUpdated, user: UserDto, user_service: UserService) -> Any:
    await user_service.update(user=user, blocked_at=None)


@router.my_chat_member(ChatMemberUpdatedFilter(LEAVE_TRANSITION))
async def bot_blocked(_: ChatMemberUpdated, user: UserDto, user_service: UserService) -> Any:
    await user_service.update(user=user, blocked_at=datetime_now())
