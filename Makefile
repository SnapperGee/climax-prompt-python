# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS ?=
SPHINXBUILD ?= poetry run sphinx-build
SOURCEDIR := source
BUILDDIR := build
DOCSDIR := $(BUILDDIR)/docs
TESTDIR := $(BUILDDIR)/test
TESTRESULTSDIR := $(TESTDIR)/results
TESTCOVERAGEDIR := $(TESTDIR)/coverage

.PHONY: help setup poetry-check ruff-check ruff-format-check mypy lint format test test-html serve-tests test-xml serve-docs readme Makefile

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(DOCSDIR)" $(SPHINXOPTS) $(O)

setup:
	poetry install
	poetry run pre-commit install

poetry-check:
	poetry check --strict --lock

ruff-check:
	poetry run ruff check ./src

ruff-format-check:
	poetry run ruff format --check ./src

mypy:
	poetry run mypy

lint: poetry-check ruff-check ruff-format-check mypy

format:
	poetry run ruff check --fix ./src
	poetry run ruff format ./src

test:
	poetry run pytest --cov=src/main --cov-report=term

test-html:
	poetry run pytest --cov=src/main \
		"--cov-report=html:$(TESTCOVERAGEDIR)/html" \
		"--html=$(TESTRESULTSDIR)/html/index.html"

serve-tests: test-html
	parallel --line-buffer --tag --halt now,done=1 ::: \
		"python -u -m http.server -b 127.0.0.1 8000 --directory $(TESTRESULTSDIR)/html" \
		"python -u -m http.server -b 127.0.0.1 8001 --directory $(TESTCOVERAGEDIR)/html"

test-xml:
	poetry run pytest --cov=src/main --cov-report=term \
		"--junitxml=$(TESTRESULTSDIR)/xml/report.xml" \
		"--cov-report=xml:$(TESTCOVERAGEDIR)/xml/coverage.xml"

serve-docs: readme html
	python -m http.server --directory $(DOCSDIR)/html -b 127.0.0.1 8000

readme:
	pandoc --from=markdown --to=rst --output=source/README.rst README.md

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(DOCSDIR)" $(SPHINXOPTS) $(O)
