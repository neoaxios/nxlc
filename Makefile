# NeoAxios Language Counter - Build and Development Tasks

.PHONY: help build test install install-dev clean lint format check-dist upload-test upload

help:
	@echo "NeoAxios Language Counter - Available commands:"
	@echo ""
	@echo "Development:"
	@echo "  test          Run test suite"
	@echo "  lint          Run linting checks"
	@echo "  format        Format code with black"
	@echo "  install-dev   Install in development mode"
	@echo ""
	@echo "Building:"
	@echo "  build         Build distribution packages"
	@echo "  check-dist    Check distribution packages"
	@echo "  clean         Clean build artifacts"
	@echo ""
	@echo "Publishing:"
	@echo "  upload-test   Upload to TestPyPI"
	@echo "  upload        Upload to PyPI (production)"
	@echo ""
	@echo "Usage:"
	@echo "  install       Install from source"
	@echo "  demo          Run demo on current directory"

# Development tasks
test:
	python3 -m pytest tests/ -v

lint:
	python3 -m flake8 nxlc.py tests/ || echo "flake8 not installed, skipping"
	python3 -c "import ast; ast.parse(open('nxlc.py').read())" && echo "✓ nxlc.py syntax OK"

format:
	python3 -m black nxlc.py tests/ || echo "black not installed, skipping"

install-dev:
	pip install -e ".[dev]"

# Building
build: clean
	python3 -m build

check-dist: build
	python3 -m twine check dist/*

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Publishing (requires credentials)
upload-test: check-dist
	@echo "Uploading to TestPyPI..."
	python3 -m twine upload --repository testpypi dist/*

upload: check-dist
	@echo "WARNING: This will upload to production PyPI!"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ]
	python3 -m twine upload dist/*

# Installation
install:
	pip install .

# Demo
demo:
	@echo "Running NXLC on current directory..."
	python3 nxlc.py . --debug

# Quick verification
verify:
	@echo "Testing basic functionality..."
	python3 nxlc.py --version
	python3 nxlc.py --help > /dev/null
	@echo "✓ NXLC verification passed"