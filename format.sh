#!/usr/bin/env sh

printf 'Formatting src directory source code with ruff...\n'
poetry run ruff format ./src && poetry run ruff check --select I --fix ./src
