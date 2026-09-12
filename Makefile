# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= poetry run sphinx-build
SOURCEDIR     = source
BUILDDIR      = build/docs

.PHONY: help setup lint format test serve Makefile

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

setup:
	poetry install
	poetry run pre-commit install

lint:
	poetry run ruff check ./src && poetry run mypy

format:
	poetry run ruff check --select I --fix ./src && poetry run ruff format ./src

test:
	poetry run pytest

serve:
	@$(MAKE) html
	python3 -m http.server --directory $(BUILDDIR)/html -b 127.0.0.1 8000

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
