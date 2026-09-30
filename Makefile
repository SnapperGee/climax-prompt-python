# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS ?=
SPHINXBUILD ?= poetry run sphinx-build
SOURCEDIR := source
CACHE_DIRS := .mypy_cache .pytest_cache .ruff_cache
BUILDDIR := build
DOCSDIR := $(BUILDDIR)/docs
TESTDIR := $(BUILDDIR)/test
TESTRESULTSDIR := $(TESTDIR)/results
TESTCOVERAGEDIR := $(TESTDIR)/coverage

.PHONY: help setup clean clean-cache clean-all poetry-check ruff-check ruff-format-check mypy lint format test test-html serve-tests test-xml readme html serve-docs Makefile

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(DOCSDIR)" $(SPHINXOPTS) $(O)

setup: ## Install dependencies and pre-commit hooks
	poetry install
	poetry run pre-commit install

clean: ## Remove build output and generated docs files
	rm -rf "$(BUILDDIR)" dist "$(SOURCEDIR)/api"
	rm -f "$(SOURCEDIR)/README.rst"

clean-cache: ## Remove tool caches and __pycache__ directories
	rm -rf $(CACHE_DIRS)
	find . \( -name .venv -o -name .git \) -prune -o \
		-type d -name __pycache__ -exec rm -rf {} +

clean-all: clean clean-cache ## Run clean and clean-cache

poetry-check: ## Validate pyproject.toml and the lock file
	poetry check --strict --lock

ruff-check: ## Lint with ruff
	poetry run ruff check ./src

ruff-format-check: ## Check formatting with ruff
	poetry run ruff format --check ./src

mypy: ## Type check with mypy
	poetry run mypy

lint: poetry-check ruff-check ruff-format-check mypy ## Run all lint and type checks

format: ## Fix lint issues and format code with ruff
	poetry run ruff check --fix ./src
	poetry run ruff format ./src

test: ## Run tests with terminal coverage report
	poetry run pytest --cov=src/main --cov-report=term

test-html: ## Run tests with HTML test and coverage reports
	poetry run pytest --cov=src/main \
		"--cov-report=html:$(TESTCOVERAGEDIR)/html" \
		"--html=$(TESTRESULTSDIR)/html/index.html"

serve-tests: test-html ## Serve HTML test and coverage reports on ports 8000 and 8001 respectively
	parallel --line-buffer --tag --halt now,done=1 ::: \
		"python3 -u -m http.server -b 127.0.0.1 8000 --directory $(TESTRESULTSDIR)/html" \
		"python3 -u -m http.server -b 127.0.0.1 8001 --directory $(TESTCOVERAGEDIR)/html"

test-xml: ## Run tests with JUnit XML and XML coverage reports
	poetry run pytest --cov=src/main --cov-report=term \
		"--junitxml=$(TESTRESULTSDIR)/xml/report.xml" \
		"--cov-report=xml:$(TESTCOVERAGEDIR)/xml/coverage.xml"

readme: ## Convert README.md to RST for Sphinx
	pandoc --from=markdown --to=rst "--output=$(SOURCEDIR)/README.rst" README.md

html: readme ## Build HTML API docs
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(DOCSDIR)" $(SPHINXOPTS) $(O)

serve-docs: html ## Build and serve HTML API docs on port 8000
	python3 -m http.server --directory "$(DOCSDIR)/html" -b 127.0.0.1 8000

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(DOCSDIR)" $(SPHINXOPTS) $(O)
