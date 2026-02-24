.PHONY: help install dev test test-unit test-playwright test-all lint format clean playwright-install

help:
	@echo "djust-admin development commands:"
	@echo ""
	@echo "  make install           Install package in development mode"
	@echo "  make dev               Install with dev dependencies"
	@echo "  make test              Run unit tests only"
	@echo "  make test-playwright   Run Playwright browser tests"
	@echo "  make test-all          Run all tests (unit + playwright)"
	@echo "  make playwright-install Install Playwright browsers"
	@echo "  make lint              Run linter"
	@echo "  make format            Format code"
	@echo "  make clean             Remove build artifacts"

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

# Run unit tests only (fast)
test:
	pytest tests/test_basic.py -v

# Alias for unit tests
test-unit:
	pytest tests/test_basic.py -v

# Run Playwright browser tests
test-playwright:
	pytest tests/test_playwright_forms.py -v --headed

# Run Playwright tests headless (CI mode)
test-playwright-ci:
	pytest tests/test_playwright_forms.py -v

# Run all tests
test-all:
	pytest tests/ -v

# Install Playwright browsers
playwright-install:
	playwright install chromium

lint:
	ruff check djust_admin tests

format:
	ruff format djust_admin tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
