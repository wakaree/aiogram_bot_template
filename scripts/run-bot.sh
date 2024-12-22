#!/usr/bin/env bash

set -e

alembic upgrade head
exec python -O -m app
