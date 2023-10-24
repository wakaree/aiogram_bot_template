
**To launch the bot:**
- Setup venv and install requirements (`pip install -r requirements.txt`)
- Configure and start redis ([» Read more](https://redis.io/docs/getting-started/))
- Fill configuration in config.yml
- Configure `telegram-bot.service` ([» Read more](https://gist.github.com/comhad/de830d6d1b7ae1f165b925492e79eac8))

**To work with the project you need to install additional dependencies:**

    pip install -r dev-requirements.txt


**To update translations or add new, you should do make l10n with specified locale, like:**

    make l10n locale=en

**Fluent Syntax Guide:** https://projectfluent.org/fluent/guide/
