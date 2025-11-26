"""Main migration orchestrator."""

from typing import Dict, Any, Optional
import json
import logging
from .parser import GraphMLParser
from .loader import FalkorDBLoader

logger = logging.getLogger(__name__)


class GraphMLFalkorDBMigrator:
    """Orchestrate GraphML to FalkorDB migration."""

    def __init__(self, graphml_filepath: str):
        """
        Initialize migrator.

        Args:
            graphml_filepath: Path to GraphML file
        """
        self.graphml_filepath = graphml_filepath
        self.parser = None
        self.loader = None
        self.config = {}

    def load_config(self, config_filepath: str) -> "GraphMLFalkorDBMigrator":
        """
        Load migration configuration from JSON file.

        Args:
            config_filepath: Path to configuration JSON file

        Returns:
            Self for method chaining
        """
        try:
            with open(config_filepath, "r") as f:
                self.config = json.load(f)
            logger.info(f"Loaded configuration from {config_filepath}")
            return self
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise

    def parse_graphml(self) -> "GraphMLFalkorDBMigrator":
        """
        Parse the GraphML file.

        Returns:
            Self for method chaining
        """
        try:
            self.parser = GraphMLParser(self.graphml_filepath)
            self.parser.parse()
            topology = self.parser.get_topology()
            logger.info(f"Parsed GraphML file: {topology}")
            return self
        except Exception as e:
            logger.error(f"Failed to parse GraphML: {e}")
            raise

    def connect_falkordb(
        self,
        host: str = "localhost",
        port: int = 6379,
        username: Optional[str] = None,
        password: Optional[str] = None,
        graph_name: str = "graphml_import",
    ) -> "GraphMLFalkorDBMigrator":
        """
        Connect to FalkorDB.

        Args:
            host: Redis host
            port: Redis port
            username: Redis username
            password: Redis password
            graph_name: FalkorDB graph name

        Returns:
            Self for method chaining
        """
        try:
            self.loader = FalkorDBLoader(
                host=host,
                port=port,
                username=username,
                password=password,
                graph_name=graph_name,
            )
            self.loader.connect()
            logger.info(f"Connected to FalkorDB")
            return self
        except Exception as e:
            logger.error(f"Failed to connect to FalkorDB: {e}")
            raise

    def migrate(self, create_indexes: bool = True) -> Dict[str, Any]:
        """
        Execute the complete migration.

        Args:
            create_indexes: Whether to create indexes for node labels

        Returns:
            Migration result summary

        Raises:
            RuntimeError: If parser or loader not initialised
        """
        if not self.parser:
            raise RuntimeError("GraphML not parsed. Call parse_graphml() first.")
        if not self.loader:
            raise RuntimeError("FalkorDB not connected. Call connect_falkordb() first.")

        try:
            # Create indexes
            if create_indexes:
                labels = self.parser.get_topology()["node_labels"]
                logger.info(f"Creating indexes for labels: {labels}")
                self.loader.create_node_indexes(labels)

            # Load nodes
            nodes = self.parser.get_nodes()
            logger.info(f"Loading {len(nodes)} nodes...")
            self.loader.load_nodes(nodes, self.config)

            # Load relationships
            edges = self.parser.get_edges()
            logger.info(f"Loading {len(edges)} relationships...")
            self.loader.load_relationships(edges, self.config)

            result = {
                "status": "success",
                "nodes_loaded": len(nodes),
                "relationships_loaded": len(edges),
                "graph_name": self.loader.graph_name,
            }
            logger.info(f"Migration completed successfully: {result}")
            return result

        except Exception as e:
            logger.error(f"Migration failed: {e}")
            raise

    def generate_config_template(self, output_filepath: str) -> None:
        """
        Generate a configuration template based on GraphML topology.

        Args:
            output_filepath: Path to save configuration template
        """
        if not self.parser:
            raise RuntimeError("GraphML not parsed. Call parse_graphml() first.")

        self.parser.save_sample_config(output_filepath)
        logger.info(f"Generated configuration template at {output_filepath}")

    def generate_topology_report(self, output_filepath: str) -> None:
        """
        Generate a topology report.

        Args:
            output_filepath: Path to save topology report
        """
        if not self.parser:
            raise RuntimeError("GraphML not parsed. Call parse_graphml() first.")

        self.parser.save_topology(output_filepath)
        logger.info(f"Generated topology report at {output_filepath}")

    def close(self) -> None:
        """Close database connection."""
        if self.loader:
            self.loader.close()
