from typing import TYPE_CHECKING, Annotated, Any, NewType, TypeAlias, Union

from aiogram.types import (
    ChatMemberAdministrator,
    ChatMemberBanned,
    ChatMemberLeft,
    ChatMemberMember,
    ChatMemberOwner,
    ChatMemberRestricted,
    ForceReply,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from pydantic import PlainValidator

if TYPE_CHECKING:
    ListStr: TypeAlias = list[str]
else:
    ListStr = NewType("ListStr", list[str])


AnyKeyboard: TypeAlias = Union[
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
]

AnyChatMember: TypeAlias = Union[
    ChatMemberOwner,
    ChatMemberAdministrator,
    ChatMemberMember,
    ChatMemberRestricted,
    ChatMemberLeft,
    ChatMemberBanned,
]

StringList: TypeAlias = Annotated[ListStr, PlainValidator(func=lambda x: x.split(","))]
Int16: TypeAlias = Annotated[int, 16]
Int32: TypeAlias = Annotated[int, 32]
Int64: TypeAlias = Annotated[int, 64]
DictStrAny: TypeAlias = dict[str, Any]
