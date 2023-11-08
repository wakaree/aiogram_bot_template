
project_dir := .
bot_dir := bot

translations_dir := translations
migrations_dir := migrations/versions


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
	  --rev-id $(shell python migrations/_get_revision_id.py) \
	  --message $(message)
