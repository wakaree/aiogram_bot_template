
project_dir := .
bot_dir := aiogram_bot_template
translations_dir := translations

# Lint code
.PHONY: lint
lint:
	@poetry run black --check --diff $(project_dir)
	@poetry run ruff $(project_dir)
	@poetry run mypy $(project_dir) --strict

# Reformat code
.PHONY: reformat
reformat:
	@poetry run black $(project_dir)
	@poetry run ruff $(project_dir) --fix

# Update translations
.PHONY: i18n
i18n:
	poetry run i18n multiple-extract \
		--input-paths $(bot_dir) \
		--output-dir $(translations_dir) \
		-k i18n -k L --locales $(locale) \
		--create-missing-dirs

# Make database migration
.PHONY: migration
migration:
	poetry run alembic revision \
	  --autogenerate \
	  --rev-id $(shell python migrations/_get_next_revision_id.py) \
	  --message $(message)

.PHONY: migrate
migrate:
	poetry run alembic upgrade head

.PHONY: app-build
app-build:
	docker-compose build

.PHONY: app-run-db
app-run-db:
	docker compose stop
	docker compose up -d redis postgres --remove-orphans

.PHONY: app-run
app-run:
	docker-compose stop
	docker-compose up -d --remove-orphans

.PHONY: app-stop
app-stop:
	docker-compose stop

.PHONY: app-down
app-down:
	docker-compose down

.PHONY: app-destroy
app-destroy:
	docker-compose down -v --remove-orphans

.PHONY: app-logs
app-logs:
	docker-compose logs -f bot
