TEST_DIRS := tests
PROJECT_DIRS := app tests
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
	@echo "Running tests"
	poetry run python -m pytest $(TEST_DIRS)


.PHONY: clean
clean:
	@echo "Cleaning project: $(CLEANED_FILES)"
	ls -R $(PROJECT_DIRS) | grep __pycache__ | xargs rm -rf