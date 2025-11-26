#!/bin/bash
# Analyse a GraphML file

set -e

if [ $# -eq 0 ]; then
    echo "Usage: analyse.sh <graphml_file>"
    echo "Example: analyse.sh my_graph.graphml"
    exit 1
fi

cd "$(dirname "$0")/.."
uv run python -m graphml_to_falkordb.cli "$1" --analyze-only
