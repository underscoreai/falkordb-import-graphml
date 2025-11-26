#!/usr/bin/env just --justfile

set dotenv-load := false

# Default recipe - show help
default:
    @just --list

# Install dependencies with uv
install:
    uv sync

# Run linter
lint:
    uv run ruff check graphml_to_falkordb/

# Format code with black
format:
    uv run black graphml_to_falkordb/

# Run tests
test:
    uv run pytest -v

# Analyse GraphML file structure
analyse FILE="test_sample.graphml":
    uv run python -m graphml_to_falkordb.cli {{FILE}} --analyze-only

# Generate configuration template
config FILE="test_sample.graphml" OUTPUT="generated_config.json":
    uv run python -m graphml_to_falkordb.cli {{FILE}} --generate-config {{OUTPUT}}

# Generate topology report
topology FILE="test_sample.graphml" OUTPUT="generated_topology.json":
    uv run python -m graphml_to_falkordb.cli {{FILE}} --generate-topology {{OUTPUT}}

# Migrate GraphML to FalkorDB
migrate FILE="test_sample.graphml" GRAPH="graphml_test" HOST="localhost" PORT="6379":
    uv run python -m graphml_to_falkordb.cli {{FILE}} \
        --host {{HOST}} \
        --port {{PORT}} \
        --graph-name {{GRAPH}}

# Clean build artifacts and cache
clean:
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete
    rm -rf .pytest_cache .mypy_cache build dist *.egg-info
    rm -f generated_config.json generated_topology.json
