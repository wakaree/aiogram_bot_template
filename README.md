
# Launching the bot
1. Setup [venv](https://docs.python.org/3/library/venv.html)
   and install requirements (`pip install -r requirements.txt`)
2. Configure and start [PostgreSQL](https://www.postgresql.org/)
3. Configure and start Redis ([» Read more](https://redis.io/docs/install/install-redis/))
4. Fill configuration in `config.yml`
5. Fill `sqlalchemy.url` in `alembic.ini`
6. Run migrations (`alembic upgrade head`)
7. Configure `telegram-bot.service` ([» Read more](https://gist.github.com/comhad/de830d6d1b7ae1f165b925492e79eac8))

# Working with project
> **Please note that additional dependencies should be installed!**

    pip install -r dev-requirements.txt

## Updating database tables structure
**Make migration script:**

    make migration message=MESSAGE_WHAT_MIGRATION_DOES

**Run migrations:**

    alembic upgrade head


## Working with translations
1. Parse new used localization keys to update translations files
   (`make l10n locale=TRANSLATION_LOCALE`)
2. Write new translations in `.ftl` files by `translations/SPECIFIED_LOCALE`
3. Restart the bot


## Useful links
- [PostgreSQL documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy documentation](https://docs.sqlalchemy.org/en/20/)
- [alembic documentation](https://alembic.sqlalchemy.org/en/latest/)
- [Redis documentation](https://redis.io/docs/)
- [Fluent Syntax Guide](https://projectfluent.org/fluent/guide/)
