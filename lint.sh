#!/usr/bin/env sh

printf 'Linting src directory source code with flake8 and mypy...\n'
poetry run flake8 && poetry run mypy
