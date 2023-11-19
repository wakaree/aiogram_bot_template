from aiogram import Bot, Dispatcher

from utils.loggers import setup_logger

from .factories import create_bot, create_dispatcher
from .runners import run_polling, run_webhook
from .settings import Settings


def main() -> None:
    setup_logger()
    settings: Settings = Settings()
    dp: Dispatcher = create_dispatcher(settings=settings)
    bot: Bot = create_bot(settings=settings)
    if settings.use_webhook:
        return run_webhook(dp=dp, bot=bot, settings=settings)
    return run_polling(dp=dp, bot=bot)


if __name__ == "__main__":
    main()
