from __future__ import annotations

import asyncio
import hashlib
import logging
from dataclasses import dataclass
from typing import Final

from aiogram import Bot, Dispatcher, loggers
from aiogram.methods import SetWebhook

from app.application.models.config import AppConfig, Assets
from app.application.ports.storages.key_value import KvStorage
from app.utils import mjson

logger: Final[logging.Logger] = logging.getLogger(name=__name__)


@dataclass(frozen=True)
class LifespanService:
    config: AppConfig
    assets: Assets
    kv_storage: KvStorage
    bot: Bot

    async def setup_polling(self, dispatcher: Dispatcher) -> None:
        await self.bot.delete_webhook(
            drop_pending_updates=self.config.telegram.drop_pending_updates,
        )
        if self.config.telegram.drop_pending_updates:
            loggers.dispatcher.info("Updates skipped successfully")
        asyncio.create_task(dispatcher.start_polling(self.bot, handle_signals=False))

    async def stop_polling(self, dispatcher: Dispatcher) -> None:
        # noinspection PyProtectedMember
        if dispatcher._running_lock.locked():
            await dispatcher.stop_polling()
            loggers.dispatcher.info("Polling stopped successfully")

    async def setup_commands(self) -> None:
        commands_data = {
            locale: [cmd.model_dump() for cmd in cmds]
            for locale, cmds in self.assets.commands.items()
        }
        commands_hash: str = hashlib.sha256(mjson.bytes_encode(commands_data)).hexdigest()

        if await self.kv_storage.is_commands_set(bot_id=self.bot.id, commands_hash=commands_hash):
            logger.info("Skipping commands setup, already set")
            return

        for locale, commands in self.assets.commands.items():
            await self.bot.set_my_commands(commands=commands, language_code=locale)

        await self.kv_storage.set_commands_lock(bot_id=self.bot.id, commands_hash=commands_hash)
        logger.info("Bot commands successfully set")

    async def setup_webhooks(self, dispatcher: Dispatcher) -> None:
        url: str = self.config.server.build_url(path=self.config.telegram.webhook_path)
        method: SetWebhook = SetWebhook(
            url=url,
            allowed_updates=dispatcher.resolve_used_update_types(),
            secret_token=self.config.telegram.webhook_secret.get_secret_value(),
            drop_pending_updates=self.config.telegram.drop_pending_updates,
        )

        webhook_hash: str = hashlib.sha256(mjson.bytes_encode(method.model_dump())).hexdigest()
        if await self.kv_storage.is_webhook_set(bot_id=self.bot.id, webhook_hash=webhook_hash):
            loggers.webhook.info("Skipping webhook setup, already set on url '%s'", url)
            return

        if not await self.bot(method):
            raise RuntimeError(f"Failed to set webhook on url '{url}'")

        await self.kv_storage.clear_webhooks(bot_id=self.bot.id)
        await self.kv_storage.set_webhook(bot_id=self.bot.id, webhook_hash=webhook_hash)
        loggers.webhook.info("Webhook successfully set on url '%s'", url)

    async def reset_webhooks(self) -> None:
        if not self.config.telegram.reset_webhook:
            return
        if await self.bot.delete_webhook():
            await self.kv_storage.clear_webhooks(bot_id=self.bot.id)
            loggers.webhook.info("Dropped webhook.")
        else:
            loggers.webhook.error("Failed to drop webhook.")
