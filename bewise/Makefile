TEST_DIRS := tests
PYTHON_FILES := app/*.py tests/*.py

.PHONY: setup
setup: pyproject.toml
	@echo "Installing project dependencies"
	poetry install --no-root

.PHONY: fmt
fmt:
	@echo "Format code"
	poetry run ruff format $(PYTHON_FILES)
	poetry run ruff check --fix $(PYTHON_FILES)

.PHONY: lint
lint:
	@echo "Linting code"
	poetry run ruff check -v $(PYTHON_FILES)

.PHONY: test
test:
	@echo "Running tests"
	poetry run python -m pytest $(TEST_DIRS)

.PHONY: ci
ci: fmt lint test

.PHONY: clean
clean:
	@echo "Cleaning project"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.py[co]" -delete
	find . -type f -name '._*' -exec rm -rf {} +