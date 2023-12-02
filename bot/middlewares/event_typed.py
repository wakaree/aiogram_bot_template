from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, ClassVar

from aiogram import BaseMiddleware, Router
from aiogram.enums import UpdateType


class EventTypedMiddleware(BaseMiddleware, ABC):
    if TYPE_CHECKING:
        __event_types__: ClassVar[list[UpdateType]]
    else:

        @property
        @abstractmethod
        def __event_types__(self) -> list[UpdateType]:
            pass

    def setup_inner(self, router: Router) -> None:
        for event_type in self.__event_types__:
            router.observers[event_type].middleware(self)

    def setup_outer(self, router: Router) -> None:
        for event_type in self.__event_types__:
            router.observers[event_type].outer_middleware(self)
