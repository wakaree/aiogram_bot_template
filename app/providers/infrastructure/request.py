from typing import cast

from aiogram import html
from aiogram.types import CallbackQuery, ErrorEvent, Message, TelegramObject, Update
from aiogram.types import User as AiogramUser
from aiogram_i18n.cores import FluentRuntimeCore
from dishka import FromDishka, Provider, Scope, provide, provide_all
from dishka.integrations.aiogram import AiogramMiddlewareData, AiogramProvider

from app.application.ports.repositories.users import UsersGateway
from app.application.ports.telegram.messages_helper import MessageHelper
from app.const import DEFAULT_LOCALE
from app.domain.user import User
from app.presentation.telegram.helpers.messages import MessageHelperImpl
from app.presentation.telegram.view.renderer import Renderer


class UserProvider(AiogramProvider):
    @provide(scope=Scope.REQUEST)
    async def provide_user(
        self,
        middleware_data: AiogramMiddlewareData,
        users_gateway: FromDishka[UsersGateway],
        core: FromDishka[FluentRuntimeCore],
    ) -> User:
        aiogram_user: AiogramUser | None = middleware_data.get("event_from_user")
        if aiogram_user is None or aiogram_user.is_bot:
            raise RuntimeError("User cannot be resolved for this handler")

        user: User | None = await users_gateway.get(user_id=aiogram_user.id)
        if user is not None:
            return user

        language: str = (
            aiogram_user.language_code
            if aiogram_user.language_code and aiogram_user.language_code in core.available_locales
            else DEFAULT_LOCALE
        )
        return await users_gateway.create(
            user_id=aiogram_user.id,
            name=html.quote(aiogram_user.full_name),
            language=language,
            language_code=aiogram_user.language_code,
        )


class MessageHelperProvider(AiogramProvider):
    @provide(scope=Scope.REQUEST)
    def provide_message_helper(
        self,
        event: TelegramObject,
        middleware_data: AiogramMiddlewareData,
    ) -> MessageHelper:
        update: TelegramObject = event
        if isinstance(update, ErrorEvent):
            update = update.update
        if isinstance(update, Update):
            update = update.event
        return MessageHelperImpl(
            update=cast(Message | CallbackQuery, update),
            bot=middleware_data["bot"],
            fsm_context=middleware_data.get("state"),
        )


class RequestInfrastructureProvider(Provider):
    scope = Scope.REQUEST

    infrastructure = provide_all(Renderer)
