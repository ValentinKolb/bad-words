.PHONY: lint format test test-cov dev run clean install-dev

install-dev:
	uv sync --locked --dev

lint:
	uv run ruff check .

format:
	uv run ruff format .

test:
	uv run pytest

test-cov:
	uv run pytest --cov=src

dev:
	uv run python main.py

run:
	uv run uvicorn main:app --host 0.0.0.0 --port 8000

# Cleanup
clean:
	rm -rf .ruff_cache
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf src/__pycache__
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".venv" -exec rm -rf {} +
