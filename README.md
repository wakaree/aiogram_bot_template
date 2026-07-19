# aiogram_bot_template
[![Author](https://img.shields.io/badge/Author-@wakaree-blue)](https://wakaree.dev)
[![License](https://img.shields.io/badge/License-MIT-blue)](#license)

## ⚙️ System dependencies
- Python 3.12+
- Docker
- docker-compose
- make
- uv

## 🐳 Quick Start with Docker compose
- Rename `.env.dist` to `.env` and configure it
- Rename `docker-compose.example.yml` to `docker-compose.yml`
- Run `make app-build` command then `make app-run` to start the bot

Use `make` to see all available commands

## 🔧 Development

### Setup environment
```bash
uv sync
```
### Update database tables structure
**Make migration script:**
```bash
make migration message=MESSAGE_WHAT_THE_MIGRATION_DOES
```
**Run migrations:**
```bash
make migrate
```

## 🚀 Used technologies:
- [uv](https://docs.astral.sh/uv/) (an extremely fast Python package and project manager)
- [Aiogram 3.x](https://github.com/aiogram/aiogram) (Telegram bot framework)
- [Dishka](https://github.com/reagento/dishka) (async DI container)
- [FastAPI](https://fastapi.tiangolo.com/) (best python web framework for building APIs)
- [PostgreSQL](https://www.postgresql.org/) (persistent relational database)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) (working with database from Python)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) (lightweight database migration tool)
- [Redis](https://redis.io/docs/) (in-memory database for FSM and caching)
- [Project Fluent](https://projectfluent.org/) (modern localization system)

## 🏗️ Project structure

Each Telegram update flows through `Handler → Flow → Interactor → Presenter → View → Renderer`:
handlers only parse the update and call a flow; flows orchestrate interactors and presenters;
interactors hold use-case logic and know nothing about Telegram; presenters build a `View`
(text + keyboard + render mode); the renderer is the only place that actually calls the Bot API.
Dependencies are wired with `dishka` and resolved via `FromDishka[...]`.

```
app/
├── domain/            # SQLAlchemy entities used directly as domain models (no DTOs)
├── application/        # Framework-agnostic core: use cases, ports (protocols), config,
│                         cache decorators, storage keys — no aiogram/FastAPI/SQLAlchemy imports
│   ├── interactors/       # use-case logic, one folder per feature
│   ├── ports/                # repository/cache/storage protocols implemented by infrastructure
│   ├── storage/keys/           # typed StorageKey[T] definitions for Redis
│   ├── models/config/            # AppConfig / Assets (env + yaml settings)
│   └── errors/                     # application/bot/HTTP error hierarchy
├── infrastructure/     # Implementations of application ports
│   ├── postgres/          # UoW, SqlRepositoryHelper[T], repositories
│   ├── redis/                # cache service + key-value repository
│   ├── localization/           # aiogram-i18n manager, Fluent helpers/patches
│   └── lifespan.py               # polling/webhook/commands setup, owned by LifespanService
├── presentation/       # Everything that talks to Telegram / HTTP
│   ├── telegram/
│   │   ├── handlers/      # thin routers — one call into a Flow per handler
│   │   ├── flows/            # orchestrate interactors + presenters, call the renderer
│   │   ├── presenters/          # build View objects (text, keyboard, render mode)
│   │   ├── view/                   # View/RenderMode/Effect models + Renderer
│   │   ├── keyboards/, callbacks/    # keyboard builders and callback data factories
│   │   ├── filters/, middlewares/       # aiogram filters and middlewares
│   │   └── helpers/                        # MessageHelper implementation
│   └── fastapi/            # webhook endpoint + healthcheck
├── providers/          # dishka Provider classes, grouped the same way as the layers above,
│                         # wired together in providers/container.py
├── runners/            # run_polling / run_webhook + FastAPI lifespan context managers
└── utils/              # framework-agnostic helpers (json, time, logging, yaml)
```

Supporting top-level directories:
- `migrations/` — Alembic migration scripts
- `assets/` — static bot assets (e.g. `commands.yml`)
- `scripts/` — dev/ops helper scripts (`run-bot.sh`, `extract-ftl.sh`)
- `nginx/`, `systemd/` — example deployment configs for reverse proxy / systemd service

## 🤝 Contributions

### 🐛 Bug Reports / ✨ Feature Requests

If you want to report a bug or request a new feature, feel free to open a [new issue](https://github.com/wakaree/aiogram_bot_template/issues/new).

### ⬇️ Pull Requests

If you want to help us improve the bot, you can create a new [Pull Request](https://github.com/wakaree/aiogram_bot_template/pulls).

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
