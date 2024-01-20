
# aiogram_bot_template

## System dependencies
- Python 3.11+
- Docker
- docker-compose
- make
- poetry

## Deployment
### Via [Docker](https://www.docker.com/)
- Rename `.env.dist` to `.env` and configure it
- Rename `docker-compose.example.yml` to `docker-compose.yml`
- Run `make app-build` command then `make app-run` to start the bot

### Via Systemd service
- Configure and start [PostgreSQL](https://www.postgresql.org/)
- Configure and start Redis ([» Read more](https://redis.io/docs/install/install-redis/))
- Rename `.env.example` to `.env` and configure it
- Run database migrations with `make migrate` command
- Configure `telegram-bot.service` ([» Read more](https://gist.github.com/comhad/de830d6d1b7ae1f165b925492e79eac8))

## Development
### Setup environment

    poetry install

### Update database tables structure
**Make migration script:**

    make migration message=MESSAGE_WHAT_THE_MIGRATION_DOES

**Run migrations:**

    make migrate


### Update translations
1. Parse new used localization keys to update translations files
   (`make i18n locale=TRANSLATION_LOCALE`)
2. Write new translations in `.ftl` files by `translations/TRANSLATION_LOCALE`
3. Restart the bot

## Used technologies:
- [Aiogram 3.x](https://github.com/aiogram/aiogram) (Telegram bot framework)
- [PostgreSQL](https://www.postgresql.org/) (database)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) (working with database from Python)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) (lightweight database migration tool)
- [Redis](https://redis.io/docs/) (in-memory data storage for FSM and caching)
- [Project Fluent](https://projectfluent.org/) (modern localization system)
