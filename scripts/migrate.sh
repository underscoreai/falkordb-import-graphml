#!/bin/bash
# Migrate a GraphML file to FalkorDB

set -e

if [ $# -lt 1 ]; then
    echo "Usage: migrate.sh <graphml_file> [--host HOST] [--port PORT] [--graph-name NAME]"
    echo "Example: migrate.sh my_graph.graphml --host localhost --port 6379 --graph-name my_db"
    exit 1
fi

cd "$(dirname "$0")/.."
uv run python -m graphml_to_falkordb.cli "$@"
