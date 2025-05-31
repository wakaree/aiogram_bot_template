from abc import ABC
from typing import ClassVar, Final

from aiogram import BaseMiddleware, Router

from app.enums.middlewares import MiddlewareEventType

DEFAULT_UPDATE_TYPES: Final[list[MiddlewareEventType]] = [
    MiddlewareEventType.MESSAGE,
    MiddlewareEventType.CALLBACK_QUERY,
    MiddlewareEventType.MY_CHAT_MEMBER,
    MiddlewareEventType.ERROR,
    MiddlewareEventType.INLINE_QUERY,
]


class EventTypedMiddleware(BaseMiddleware, ABC):
    __event_types__: ClassVar[list[str]] = []

    def get_event_types(self, router: Router) -> list[str]:
        return self.__event_types__ or router.resolve_used_update_types()

    def setup_inner(self, router: Router) -> None:
        for event_type in self.get_event_types(router=router):
            router.observers[event_type].middleware(self)

    def setup_outer(self, router: Router) -> None:
        for event_type in self.get_event_types(router=router):
            router.observers[event_type].outer_middleware(self)
