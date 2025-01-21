.PHONY: setup
setup: pyproject.toml
	@echo "Installing project dependencies"
	poetry install --no-root

.PHONY: fmt
fmt:
	@echo "Format code"

.PHONY: test
test: tests/*.py
	@echo "Run tests"


.PHONY: clean
clean:
	@echo "Cleaning project"
	# remove all the unused files