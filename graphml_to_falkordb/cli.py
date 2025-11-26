"""Command-line interface for GraphML to FalkorDB migration."""

import argparse
import logging
import sys
from .migrator import GraphMLFalkorDBMigrator


def setup_logging(verbose: bool = False) -> None:
    """
    Setup logging configuration.

    Args:
        verbose: Enable verbose logging
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Migrate GraphML files to FalkorDB"
    )

    # File arguments
    parser.add_argument("graphml_file", help="Path to GraphML file")
    parser.add_argument(
        "--config",
        help="Path to migration configuration JSON file",
        default=None,
    )

    # FalkorDB connection arguments
    parser.add_argument(
        "--host",
        help="FalkorDB host",
        default="localhost",
    )
    parser.add_argument(
        "--port",
        help="FalkorDB port",
        type=int,
        default=6379,
    )
    parser.add_argument(
        "--username",
        help="Redis username",
        default=None,
    )
    parser.add_argument(
        "--password",
        help="Redis password",
        default=None,
    )
    parser.add_argument(
        "--graph-name",
        help="FalkorDB graph name",
        default="graphml_import",
    )

    # Operation mode arguments
    parser.add_argument(
        "--analyze-only",
        action="store_true",
        help="Only analyse topology without loading to FalkorDB",
    )
    parser.add_argument(
        "--generate-config",
        metavar="OUTPUT_FILE",
        help="Generate configuration template and exit",
    )
    parser.add_argument(
        "--generate-topology",
        metavar="OUTPUT_FILE",
        help="Generate topology report and exit",
    )
    parser.add_argument(
        "--no-indexes",
        action="store_true",
        help="Skip index creation",
    )

    # Other arguments
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()
    setup_logging(args.verbose)

    try:
        # Initialise migrator
        migrator = GraphMLFalkorDBMigrator(args.graphml_file)

        # Parse GraphML
        migrator.parse_graphml()
        topology = migrator.parser.get_topology()
        print(f"\nGraphML Analysis:")
        print(f"  Nodes: {topology['node_count']}")
        print(f"  Relationships: {topology['edge_count']}")
        print(f"  Node labels: {', '.join(topology['node_labels'])}")
        print(f"  Relationship types: {', '.join(topology['relationship_types'])}")

        # Handle topology generation
        if args.generate_topology:
            migrator.generate_topology_report(args.generate_topology)
            print(f"\nTopology report saved to {args.generate_topology}")
            return

        # Handle config generation
        if args.generate_config:
            migrator.generate_config_template(args.generate_config)
            print(f"\nConfiguration template saved to {args.generate_config}")
            return

        # Handle analyse-only mode
        if args.analyze_only:
            print("\nAnalyse-only mode. Exiting without loading to FalkorDB.")
            return

        # Load configuration if provided
        if args.config:
            migrator.load_config(args.config)

        # Connect to FalkorDB
        print(f"\nConnecting to FalkorDB at {args.host}:{args.port}...")
        migrator.connect_falkordb(
            host=args.host,
            port=args.port,
            username=args.username,
            password=args.password,
            graph_name=args.graph_name,
        )

        # Execute migration
        print(f"\nStarting migration to graph '{args.graph_name}'...")
        result = migrator.migrate(create_indexes=not args.no_indexes)

        print(f"\nMigration completed successfully!")
        print(f"  Nodes loaded: {result['nodes_loaded']}")
        print(f"  Relationships loaded: {result['relationships_loaded']}")
        print(f"  Graph: {result['graph_name']}")

        migrator.close()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
