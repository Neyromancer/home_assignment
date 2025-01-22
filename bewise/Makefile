TEST_DIRS := tests
PROJECT_DIRS := app/* tests/*
PYTHON_FILES := app/*.py tests/*.py

.PHONY: setup
setup: pyproject.toml
	@echo "Installing project dependencies"
	poetry install --no-root

.PHONY: fmt
fmt:
	@echo "Format code in ${PYTHON_FILES}"
	poetry run ruff format $(PYTHON_FILES)

.PHONY: test
test: $(TEST_DIRS)/*.py
	@echo "Validating files"
	poetry run ruff check -v $(PYTHON_FILES)

	@echo "Running tests"
	poetry run python -m pytest $(TEST_DIRS)


.PHONY: clean
clean:
	@echo "Cleaning project"
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf