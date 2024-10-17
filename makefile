PYTHON_FILES = velib2strava

.PHONY: install
install:
	poetry install

.PHONY: lint
lint:
	poetry run black $(PYTHON_FILES)
	poetry run ruff check $(PYTHON_FILES) --fix
	poetry run mypy $(PYTHON_FILES)

.PHONY: clean
clean:
	rm -rf __pycache__ .mypy_cache .ruff_cache
