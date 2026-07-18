from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.application.ports.telegram.messages_helper import MessageHelper
from app.presentation.telegram.view.models import RenderMode, View


@dataclass
class Renderer:
    helper: MessageHelper

    async def apply(self, view: View) -> Any:
        if view.mode is RenderMode.NONE or view.text is None:
            return None

        if view.mode is RenderMode.NEW:
            return await self.helper.send_new_message(
                chat_id=view.chat_id,
                message_id=view.message_id,
                text=view.text,
                reply_markup=view.reply_markup,
                delete=view.delete,
                **(view.kwargs or {}),
            )

        return await self.helper.answer(
            chat_id=view.chat_id,
            message_id=view.message_id,
            text=view.text,
            reply_markup=view.reply_markup,
            edit=view.edit,
            reply=view.reply,
            delete=view.delete,
            force_edit=view.force_edit,
            **(view.kwargs or {}),
        )
