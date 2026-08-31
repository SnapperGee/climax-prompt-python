#!/usr/bin/env sh

printf 'Formatting src directory source code with black and isort...\n'
poetry run black --target-version py314 src && poetry run isort src
