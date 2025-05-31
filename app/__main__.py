from aiogram import Bot, Dispatcher

from app.factory import create_app_config, create_bot, create_dispatcher
from app.models.config import AppConfig
from app.runners.app import run_polling, run_webhook
from app.utils.logging import setup_logger


def main() -> None:
    setup_logger()
    config: AppConfig = create_app_config()
    bot: Bot = create_bot(config=config)
    dispatcher: Dispatcher = create_dispatcher(config=config)
    if config.telegram.use_webhook:
        return run_webhook(dispatcher=dispatcher, bot=bot, config=config)
    return run_polling(dispatcher=dispatcher, bot=bot, config=config)


if __name__ == "__main__":
    main()
