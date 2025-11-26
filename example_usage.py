"""Example usage of GraphML to FalkorDB migration."""

from graphml_to_falkordb import GraphMLFalkorDBMigrator
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Example 1: Basic migration with defaults
def basic_migration():
    """Basic migration with minimal configuration."""
    migrator = GraphMLFalkorDBMigrator("path/to/your/graph.graphml")

    # Parse GraphML and analyse topology
    migrator.parse_graphml()
    topology = migrator.parser.get_topology()
    print(f"Graph has {topology['node_count']} nodes and {topology['edge_count']} edges")

    # Connect to FalkorDB
    migrator.connect_falkordb(
        host="localhost",
        port=6379,
        graph_name="my_graph",
    )

    # Execute migration
    result = migrator.migrate()
    print(f"Loaded {result['nodes_loaded']} nodes and {result['relationships_loaded']} relationships")

    migrator.close()


# Example 2: Migration with custom configuration
def migration_with_config():
    """Migration with custom label and property mappings."""
    migrator = GraphMLFalkorDBMigrator("path/to/your/graph.graphml")

    # Parse GraphML
    migrator.parse_graphml()

    # Load custom configuration
    migrator.load_config("config.json")

    # Connect and migrate
    migrator.connect_falkordb(
        host="localhost",
        port=6379,
        username="default",
        password="your_password",
        graph_name="custom_graph",
    )

    result = migrator.migrate(create_indexes=True)
    migrator.close()


# Example 3: Generate configuration template
def generate_config_template():
    """Analyse GraphML and generate configuration template."""
    migrator = GraphMLFalkorDBMigrator("path/to/your/graph.graphml")

    # Parse and generate template
    migrator.parse_graphml()
    migrator.generate_config_template("generated_config.json")
    migrator.generate_topology_report("topology_report.json")

    print("Configuration template generated. Edit it and use it for custom migration.")


# Example 4: Analyse-only mode
def analyse_only():
    """Analyse GraphML without loading to FalkorDB."""
    migrator = GraphMLFalkorDBMigrator("path/to/your/graph.graphml")

    migrator.parse_graphml()
    topology = migrator.parser.get_topology()

    print("Graph Topology:")
    print(f"  Node labels: {topology['node_labels']}")
    print(f"  Relationship types: {topology['relationship_types']}")
    print(f"  Total nodes: {topology['node_count']}")
    print(f"  Total relationships: {topology['edge_count']}")


# Example 5: Programmatic usage with direct classes
def direct_class_usage():
    """Use the classes directly without the migrator."""
    from graphml_to_falkordb import GraphMLParser, FalkorDBLoader

    # Parse GraphML
    parser = GraphMLParser("path/to/your/graph.graphml")
    parser.parse()

    nodes = parser.get_nodes()
    edges = parser.get_edges()

    print(f"Parsed {len(nodes)} nodes and {len(edges)} edges")

    # Load to FalkorDB
    loader = FalkorDBLoader(host="localhost", port=6379, graph_name="direct_load")
    loader.connect()
    loader.create_node_indexes(parser.get_topology()["node_labels"])
    loader.load_nodes(nodes)
    loader.load_relationships(edges)
    loader.close()


if __name__ == "__main__":
    # Uncomment the example you want to run
    # basic_migration()
    # migration_with_config()
    # generate_config_template()
    # analyse_only()
    # direct_class_usage()
    pass
