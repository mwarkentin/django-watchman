# List available recipes
default:
    @just --list

# Clean all
clean: clean-build clean-pyc

# Clean build artifacts
clean-build:
    rm -fr build/
    rm -fr dist/
    rm -fr *.egg-info

# Clean compiled python files
clean-pyc:
    find . -name '*.pyc' -exec rm -f {} +
    find . -name '*.pyo' -exec rm -f {} +
    find . -name '*~' -exec rm -f {} +

# Check code with ruff
lint:
    uv run ruff check .
    uv run ruff format --check .

# Format code with ruff
fmt:
    uv run ruff format .
    uv run ruff check --fix .

# Run tests
test:
    uv run coverage run --parallel --source watchman -m pytest

# Serve MkDocs documentation locally
docs:
    uv run --group docs mkdocs serve

# Build MkDocs documentation
docs-build:
    uv run --group docs mkdocs build --strict

# Package and upload a release
release: clean lint test
    uv build
    uv publish

# Package a release
dist: clean lint test
    uv build
    ls -l dist

# Build and run sample project with docker
run:
    docker build -t watchman .
    docker run -it -p 8000:8000 watchman
