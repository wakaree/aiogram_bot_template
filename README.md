
# Deployment

## Via [Docker](https://www.docker.com/)
1. Rename `.env.dist` to `.env` and configure it
2. Rename `docker-compose.example.yml` to `docker-compose.yml`
3. Run `make app-build` command then `make app-run` to start the bot

## Via Systemd service
1. Setup [venv](https://docs.python.org/3/library/venv.html)
   and install requirements (`pip install -r requirements.txt`)
2. Configure and start [PostgreSQL](https://www.postgresql.org/)
3. Configure and start Redis ([» Read more](https://redis.io/docs/install/install-redis/))
4. Rename `.env.example` to `.env` and configure it
5. Run database migrations with `make migrate` command
6. Configure `telegram-bot.service` ([» Read more](https://gist.github.com/comhad/de830d6d1b7ae1f165b925492e79eac8))

# Development
> **Please note that additional dependencies should be installed!**

    pip install -r dev-requirements.txt

## Update database tables structure
**Make migration script:**

    make migration message=MESSAGE_WHAT_THE_MIGRATION_DOES

**Run migrations:**

    make migrate


## Update translations
1. Parse new used localization keys to update translations files
   (`make l10n locale=TRANSLATION_LOCALE`)
2. Write new translations in `.ftl` files by `translations/TRANSLATION_LOCALE`
3. Restart the bot


# Used technologies:
- [Aiogram 3.x](https://github.com/aiogram/aiogram) (Telegram Bot framework)
- [PostgreSQL](https://www.postgresql.org/) (database)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) (working with database from Python)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) (lightweight database migration tool)
- [Redis](https://redis.io/docs/) (in-memory data storage for FSM and caching)
- [Project Fluent](https://projectfluent.org/) (modern localization system)
