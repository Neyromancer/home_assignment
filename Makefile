TEST_DIRS := tests

.PHONY: setup
setup: pyproject.toml
	@echo "Installing project dependencies"
	poetry install --no-root

.PHONY: fmt
fmt:
	@echo "Format code"

.PHONY: test
test: $(TEST_DIRS)/*.py
	@echo "Running tests"
	poetry run python -m pytest $(TEST_DIRS)


.PHONY: clean
clean:
	@echo "Cleaning project"
	# remove all the unused files