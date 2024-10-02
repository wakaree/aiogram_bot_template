#!/usr/bin/env bash

set -e

make migrate
exec make run
