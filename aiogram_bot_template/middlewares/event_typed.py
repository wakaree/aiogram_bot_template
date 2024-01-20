from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, ClassVar

from aiogram import BaseMiddleware, Router

from ..enums import MiddlewareEventType


class EventTypedMiddleware(BaseMiddleware, ABC):
    if TYPE_CHECKING:
        __event_types__: ClassVar[list[MiddlewareEventType]]
    else:

        @property
        @abstractmethod
        def __event_types__(self) -> list[MiddlewareEventType]:
            pass

    def setup_inner(self, router: Router) -> None:
        for event_type in self.__event_types__:
            router.observers[event_type].middleware(self)

    def setup_outer(self, router: Router) -> None:
        for event_type in self.__event_types__:
            router.observers[event_type].outer_middleware(self)
