
project_dir := .
package_dir := app

.PHONY: help
help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Formatting & Linting

.PHONY: reformat
reformat: ## Reformat code
	@uv run ruff format $(project_dir)
	@uv run ruff check $(project_dir) --fix

.PHONY: lint
lint: reformat ## Lint code
	@uv run mypy $(project_dir)

##@ Database

.PHONY: migration
migration: ## Make database migration
	@uv run alembic revision \
	  --autogenerate \
	  --rev-id $(shell python migrations/_get_revision_id.py) \
	  --message $(message)

.PHONY: migrate
migrate: ## Apply database migrations
	@uv run alembic upgrade head

.PHONY: app-run-db
app-run-db: ## Run bot database containers
	@docker compose up -d --remove-orphans postgres redis

##@ App commands

.PHONY: run
run: ## Run bot
	@uv run python -O -m $(package_dir)

.PHONY: app-build
app-build: ## Build bot image
	@docker compose build

.PHONY: app-run
app-run: ## Run bot in docker container
	@docker compose stop
	@docker compose up -d --remove-orphans

.PHONY: app-stop
app-stop: ## Stop docker containers
	@docker compose stop

.PHONY: app-down
app-down: ## Down docker containers
	@docker compose down

.PHONY: app-destroy
app-destroy: ## Destroy docker containers
	@docker compose down -v --remove-orphans

.PHONY: app-logs
app-logs: ## Show bot logs
	@docker compose logs -f bot

##@ Other

.PHONY: name
name: ## Get top-level package name
	@echo $(package_dir)
