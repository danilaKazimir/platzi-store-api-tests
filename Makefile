.PHONY: check format format-check lint test type-check

check: lint format-check type-check

lint:
	uv run ruff check .

format-check:
	uv run ruff format --check .

type-check:
	uv run mypy

test:
	uv run pytest -s -v -n auto

format:
	uv run ruff format .
	uv run ruff check . --fix
