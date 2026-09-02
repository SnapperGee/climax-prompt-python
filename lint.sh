#!/usr/bin/env sh

printf 'Linting src directory source code with ruff and mypy...\n'
poetry run ruff check ./src && poetry run mypy
