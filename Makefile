# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS ?=
SPHINXBUILD ?= poetry run sphinx-build
SOURCEDIR := source
BUILDDIR := build/docs
TESTBUILDDIR := build/test
TESTREPORTBUILDDIR := $(TESTBUILDDIR)/report
TESTCOVERAGEBUILDDIR := $(TESTBUILDDIR)/coverage

.PHONY: help setup lint format test test-html serve-tests test-xml serve-docs readme Makefile

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

setup:
	poetry install
	poetry run pre-commit install

lint:
	poetry run ruff check --extend-select I ./src && poetry run ruff format --check ./src && poetry run mypy

format:
	poetry run ruff check --extend-select I --fix ./src && poetry run ruff format ./src

test:
	poetry run pytest --cov=src/main --cov-report=term

test-html:
	poetry run pytest --cov=src/main \
		"--cov-report=html:$(TESTCOVERAGEBUILDDIR)/html" \
		"--html=$(TESTREPORTBUILDDIR)/html/index.html"

serve-tests:
	@$(MAKE) test-html
	parallel --line-buffer --tag --halt now,done=1 ::: \
		"python -u -m http.server -b 127.0.0.1 8000 --directory $(TESTREPORTBUILDDIR)/html" \
		"python -u -m http.server -b 127.0.0.1 8001 --directory $(TESTCOVERAGEBUILDDIR)/html"

test-xml:
	poetry run pytest --cov=src/main --cov-report=term \
		"--junitxml=$(TESTREPORTBUILDDIR)/xml/report.xml" \
		"--cov-report=xml:$(TESTCOVERAGEBUILDDIR)/xml/coverage.xml"

serve-docs:
	@$(MAKE) html
	python -m http.server --directory $(BUILDDIR)/html -b 127.0.0.1 8000

readme:
	poetry run pandoc --from=markdown --to=rst --output=source/README.rst README.md

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
