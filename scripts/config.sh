#!/bin/bash
# Generate configuration template from GraphML file

set -e

if [ $# -lt 1 ]; then
    echo "Usage: config.sh <graphml_file> [output_file]"
    echo "Example: config.sh my_graph.graphml config.json"
    exit 1
fi

GRAPHML_FILE="$1"
OUTPUT_FILE="${2:-generated_config.json}"

cd "$(dirname "$0")/.."
uv run python -m graphml_to_falkordb.cli "$GRAPHML_FILE" --generate-config "$OUTPUT_FILE"
echo "Configuration template saved to: $OUTPUT_FILE"
