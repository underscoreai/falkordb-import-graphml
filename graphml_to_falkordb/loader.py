"""FalkorDB loader module."""

from typing import Dict, List, Any, Optional
import json
from falkordb import FalkorDB
import logging

logger = logging.getLogger(__name__)


class FalkorDBLoader:
    """Load graph data into FalkorDB."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        username: Optional[str] = None,
        password: Optional[str] = None,
        graph_name: str = "graphml_import",
        db_index: int = 0,
    ):
        """
        Initialize FalkorDB loader.

        Args:
            host: Redis host address
            port: Redis port
            username: Redis username (optional)
            password: Redis password (optional)
            graph_name: Name of the FalkorDB graph
            db_index: Redis database index
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.graph_name = graph_name
        self.db_index = db_index
        self.db = None
        self.graph = None
        self.node_map = {}  # Map from original ID to FalkorDB internal ID

    def connect(self) -> "FalkorDBLoader":
        """
        Connect to FalkorDB.

        Returns:
            Self for method chaining

        Raises:
            ConnectionError: If connection fails
        """
        try:
            self.db = FalkorDB(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
            )
            self.graph = self.db.select_graph(self.graph_name)
            logger.info(f"Connected to FalkorDB graph: {self.graph_name}")
            return self
        except Exception as e:
            logger.error(f"Failed to connect to FalkorDB: {e}")
            raise ConnectionError(f"Failed to connect to FalkorDB: {e}")

    def create_node_indexes(self, labels: List[str]) -> None:
        """
        Create indexes for node labels.

        Args:
            labels: List of node labels to create indexes for
        """
        for label in labels:
            try:
                self.graph.query(f"CREATE INDEX ON :{label}(id)")
                logger.debug(f"Created index on :{label}(id)")
            except Exception as e:
                logger.warning(f"Index creation failed for {label}: {e}")

    def load_nodes(
        self,
        nodes: List[Dict[str, Any]],
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Load nodes into FalkorDB.

        Args:
            nodes: List of node dictionaries with 'id', 'label', and properties
            config: Optional configuration for label/property mappings
        """
        config = config or {}
        node_label_mappings = config.get("node_labels", {})

        for node in nodes:
            node_id = node["id"]
            label = node["label"]

            # Apply label mapping if configured
            target_label = label
            if label in node_label_mappings:
                target_label = node_label_mappings[label].get("target_label", label)

            # Build property mapping
            properties = {}
            for key, value in node.items():
                if key not in ["id", "label"]:
                    properties[key] = value

            # Apply property mappings if configured
            if label in node_label_mappings:
                prop_mappings = node_label_mappings[label].get("property_mappings", {})
                for old_key, new_key in prop_mappings.items():
                    if old_key in properties:
                        properties[new_key] = properties.pop(old_key)

            # Create Cypher query
            props_str = ", ".join(
                f"{k}: {self._format_value(v)}" for k, v in properties.items()
            )
            if props_str:
                query = (
                    f"CREATE (n:{target_label} {{id: '{node_id}', {props_str}}})"
                )
            else:
                query = f"CREATE (n:{target_label} {{id: '{node_id}'}})"

            try:
                self.graph.query(query)
                self.node_map[node_id] = node_id
                logger.debug(f"Created node {node_id} with label {target_label}")
            except Exception as e:
                logger.error(f"Failed to create node {node_id}: {e}")
                raise

    def load_relationships(
        self,
        relationships: List[Dict[str, Any]],
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Load relationships into FalkorDB.

        Args:
            relationships: List of relationship dictionaries with source_id, target_id, type, and properties
            config: Optional configuration for relationship/property mappings
        """
        config = config or {}
        rel_mappings = config.get("relationship_types", {})

        for rel in relationships:
            source_id = rel["source_id"]
            target_id = rel["target_id"]
            rel_type = rel["type"]

            # Apply relationship type mapping if configured
            target_rel_type = rel_type
            if rel_type in rel_mappings:
                target_rel_type = rel_mappings[rel_type].get("target_type", rel_type)

            # Build property mapping
            properties = {}
            for key, value in rel.items():
                if key not in ["source_id", "target_id", "type"]:
                    properties[key] = value

            # Apply property mappings if configured
            if rel_type in rel_mappings:
                prop_mappings = rel_mappings[rel_type].get("property_mappings", {})
                for old_key, new_key in prop_mappings.items():
                    if old_key in properties:
                        properties[new_key] = properties.pop(old_key)

            # Create Cypher query
            props_str = ", ".join(
                f"{k}: {self._format_value(v)}" for k, v in properties.items()
            )
            if props_str:
                query = f"MATCH (s {{id: '{source_id}'}}), (t {{id: '{target_id}'}}) CREATE (s)-[:{target_rel_type} {{{props_str}}}]->(t)"
            else:
                query = f"MATCH (s {{id: '{source_id}'}}), (t {{id: '{target_id}'}}) CREATE (s)-[:{target_rel_type}]->(t)"

            try:
                self.graph.query(query)
                logger.debug(
                    f"Created relationship {source_id}-[{target_rel_type}]->{target_id}"
                )
            except Exception as e:
                logger.error(
                    f"Failed to create relationship {source_id}-[{rel_type}]->{target_id}: {e}"
                )
                raise

    def get_graph_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the loaded graph.

        Returns:
            Dictionary with node and relationship counts
        """
        try:
            result = self.graph.query("RETURN COUNT(*) as nodes, COUNT(*) as rels")
            return {
                "nodes": len(self.node_map),
                "relationships": "See query logs",
            }
        except Exception as e:
            logger.error(f"Failed to get graph stats: {e}")
            return {}

    def close(self) -> None:
        """Close database connection."""
        if self.db:
            self.db.connection.close()
            logger.info("Disconnected from FalkorDB")

    @staticmethod
    def _format_value(value: Any) -> str:
        """
        Format a Python value for Cypher query.

        Args:
            value: Python value to format

        Returns:
            Formatted string for Cypher
        """
        if isinstance(value, str):
            # Escape single quotes
            escaped = value.replace("'", "\\'")
            return f"'{escaped}'"
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, list):
            formatted_items = [FalkorDBLoader._format_value(item) for item in value]
            return f"[{', '.join(formatted_items)}]"
        elif value is None:
            return "null"
        else:
            return f"'{str(value)}'"
