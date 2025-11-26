# GraphML to FalkorDB Migration Tool

A Python-based tool for migrating graph data from GraphML files to FalkorDB, inspired by the Neo4j to FalkorDB migration tools.

## Quick Start

Get up and running in 3 minutes:

### 1. Install Dependencies

```bash
uv sync
```

### 2. Choose Your Interface

Pick one:

- **Just** (recommended): `just analyse`
- **Shell script**: `./scripts/analyse.sh test_sample.graphml`
- **Raw UV**: `uv run python -m graphml_to_falkordb.cli test_sample.graphml --analyze-only`

### 3. Your First Analysis

```bash
just analyse
```

Output:
```
GraphML Analysis:
  Nodes: 3
  Relationships: 3
  Node labels: Company, Person
  Relationship types: KNOWS, WORKS_AT

Analyse-only mode. Exiting without loading to FalkorDB.
```

### 4. Generate Configuration

```bash
just config
```

Creates `generated_config.json` for customising mappings.

### 5. Migrate to FalkorDB

```bash
just migrate
```

Requires running FalkorDB instance on `localhost:6379`.

## Full Workflow

```bash
just analyse my_graph.graphml      # Analyse structure
just config my_graph.graphml       # Generate config template
vi generated_config.json           # Edit if needed
just migrate my_graph.graphml      # Migrate to FalkorDB
```

---

## Features

- **GraphML Parsing**: Uses NetworkX to read and parse GraphML files, similar to how NetworkX handles graph data
- **FalkorDB Loading**: Batch loading of nodes and relationships into FalkorDB using Cypher queries
- **Configuration-Driven**: Support for custom label and property mappings via JSON configuration
- **Topology Analysis**: Analyse and report on graph structure before migration
- **CLI Tool**: Command-line interface for easy integration into workflows
- **Programmable API**: Use the classes directly for programmatic access

## Programmatic Usage

```python
from graphml_to_falkordb import GraphMLFalkorDBMigrator

# Create migrator
migrator = GraphMLFalkorDBMigrator("path/to/graph.graphml")

# Parse GraphML
migrator.parse_graphml()

# Connect to FalkorDB
migrator.connect_falkordb(host="localhost", port=6379, graph_name="my_graph")

# Execute migration
result = migrator.migrate()
print(f"Loaded {result['nodes_loaded']} nodes and {result['relationships_loaded']} edges")

migrator.close()
```

## API Overview

### GraphMLParser

Parses GraphML files using NetworkX.

```python
from graphml_to_falkordb import GraphMLParser

parser = GraphMLParser("path/to/graph.graphml")
parser.parse()

# Get data
nodes = parser.get_nodes()
edges = parser.get_edges()
topology = parser.get_topology()

# Generate templates
parser.save_sample_config("config.json")
parser.save_topology("topology.json")
```

### FalkorDBLoader

Loads data into FalkorDB.

```python
from graphml_to_falkordb import FalkorDBLoader

loader = FalkorDBLoader(
    host="localhost",
    port=6379,
    graph_name="my_graph"
)

loader.connect()
loader.create_node_indexes(["Person", "Company"])
loader.load_nodes(nodes)
loader.load_relationships(edges)
loader.close()
```

### GraphMLFalkorDBMigrator

Orchestrates the complete migration workflow.

```python
from graphml_to_falkordb import GraphMLFalkorDBMigrator

migrator = GraphMLFalkorDBMigrator("path/to/graph.graphml")
migrator.parse_graphml()
migrator.load_config("config.json")  # Optional
migrator.connect_falkordb(host="localhost", port=6379)
result = migrator.migrate()
migrator.close()
```

## Configuration

Create a JSON configuration file to customise label and property mappings:

```json
{
  "node_labels": {
    "Person": {
      "target_label": "Person",
      "property_mappings": {
        "old_name": "name"
      }
    }
  },
  "relationship_types": {
    "WORKS_AT": {
      "target_type": "WORKS_AT",
      "property_mappings": {
        "old_date": "start_date"
      }
    }
  }
}
```

## CLI Options

```
usage: graphml-to-falkordb [-h] [--config CONFIG]
                           [--host HOST] [--port PORT]
                           [--username USERNAME] [--password PASSWORD]
                           [--graph-name GRAPH_NAME]
                           [--analyze-only]
                           [--generate-config OUTPUT_FILE]
                           [--generate-topology OUTPUT_FILE]
                           [--no-indexes] [-v]
                           graphml_file

Migrate GraphML files to FalkorDB

positional arguments:
  graphml_file              Path to GraphML file

optional arguments:
  -h, --help                Show this help message and exit
  --config CONFIG           Path to migration configuration JSON file
  --host HOST               FalkorDB host (default: localhost)
  --port PORT               FalkorDB port (default: 6379)
  --username USERNAME       Redis username
  --password PASSWORD       Redis password
  --graph-name GRAPH_NAME   FalkorDB graph name (default: graphml_import)
  --analyze-only            Only analyse topology without loading
  --generate-config OUTPUT  Generate configuration template and exit
  --generate-topology OUTPUT Generate topology report and exit
  --no-indexes              Skip index creation
  -v, --verbose             Enable verbose logging
```

## Architecture

The tool follows a similar architecture to the FalkorDB Neo4j migration tools:

1. **GraphMLParser**: Reads GraphML files using NetworkX and extracts nodes, edges, and topology
2. **FalkorDBLoader**: Manages FalkorDB connections and batch loading via Cypher queries
3. **GraphMLFalkorDBMigrator**: Orchestrates the complete workflow with optional configuration

## GraphML Format Support

The tool expects GraphML files with:
- `label` or `type` attributes for node labels and relationship types
- Properties stored as additional XML attributes
- Node IDs as the primary identifier

Example GraphML structure:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns">
  <graph id="G" edgedefault="directed">
    <node id="1" label="Person">
      <data key="name">Alice</data>
    </node>
    <edge id="e1" source="1" target="2" label="KNOWS">
      <data key="since">2020</data>
    </edge>
  </graph>
</graphml>
```

## Examples

See `example_usage.py` for detailed usage examples including:
- Basic migration
- Migration with custom configuration
- Configuration template generation
- Analyse-only mode
- Direct class usage

## Requirements

- Python 3.8+
- NetworkX 2.6+
- FalkorDB 1.0+
- Redis 4.0+

## License

MIT
