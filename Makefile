
project_dir := .
bot_dir := bot

translations_dir := translations


# Lint code
.PHONY: lint
lint:
	@black --check --diff $(project_dir)
	@ruff $(project_dir)
	@mypy $(project_dir) --strict

# Reformat code
.PHONY: reformat
reformat:
	@black $(project_dir)
	@ruff $(project_dir) --fix

# Update translations
.PHONY: l10n
l10n:
	i18n multiple-extract \
		--input-paths $(bot_dir) \
		--output-dir $(translations_dir) \
		-k l10n -k L --locales $(locale) \
		--create-missing-dirs

# Make database migration
.PHONY: migration
migration:
	alembic revision \
	  --autogenerate \
	  --rev-id $(shell python migrations/_get_next_revision_id.py) \
	  --message $(message)

.PHONY: migrate
	alembic upgrade head

.PHONY: app-build
app-build:
	docker-compose build

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
