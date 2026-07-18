from typing import Any, Awaitable, Callable

from aiogram.types import TelegramObject
from dishka import AsyncContainer
from dishka.integrations.aiogram import CONTAINER_NAME, AiogramMiddlewareData

from app.presentation.telegram.middlewares.event_typed import EventTypedMiddleware


class UpdateContainerContextMiddleware(EventTypedMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        container: AsyncContainer = data[CONTAINER_NAME]
        # noinspection PyProtectedMember
        container._context.update({AiogramMiddlewareData: data})  # type: ignore
        return await handler(event, data)
