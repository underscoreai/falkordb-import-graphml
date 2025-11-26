"""GraphML parser module using networkx."""

import networkx as nx
from typing import Dict, List, Tuple, Any, Optional
import json


class GraphMLParser:
    """Parse GraphML files and extract graph data."""

    def __init__(self, filepath: str):
        """
        Initialize parser with GraphML file.

        Args:
            filepath: Path to GraphML file
        """
        self.filepath = filepath
        self.graph = None
        self.nodes_data = []
        self.edges_data = []
        self.node_labels = set()
        self.relationship_types = set()

    def parse(self) -> "GraphMLParser":
        """
        Parse the GraphML file.

        Returns:
            Self for method chaining
        """
        self.graph = nx.read_graphml(self.filepath)
        self._extract_nodes()
        self._extract_edges()
        return self

    def _extract_nodes(self) -> None:
        """Extract nodes from graph with their properties."""
        for node_id, attributes in self.graph.nodes(data=True):
            node_data = {"id": node_id}

            # Extract label (default to "Node" if not specified)
            label = attributes.get("label", attributes.get("type", "Node"))
            node_data["label"] = label
            self.node_labels.add(label)

            # Extract all other properties
            for key, value in attributes.items():
                if key not in ["label", "type"]:
                    node_data[key] = value

            self.nodes_data.append(node_data)

    def _extract_edges(self) -> None:
        """Extract edges from graph with their properties."""
        # Check if it's a multigraph
        is_multigraph = isinstance(self.graph, nx.MultiGraph) or isinstance(
            self.graph, nx.MultiDiGraph
        )

        if is_multigraph:
            edge_iterator = self.graph.edges(data=True, keys=True)
        else:
            edge_iterator = self.graph.edges(data=True)

        for edge_tuple in edge_iterator:
            if is_multigraph:
                source, target, key, attributes = edge_tuple
            else:
                source, target, attributes = edge_tuple

            edge_data = {
                "source_id": source,
                "target_id": target,
            }

            # Extract relationship type (default to "RELATES_TO" if not specified)
            rel_type = attributes.get("label", attributes.get("type", "RELATES_TO"))
            edge_data["type"] = rel_type
            self.relationship_types.add(rel_type)

            # Extract all other properties
            for key, value in attributes.items():
                if key not in ["label", "type"]:
                    edge_data[key] = value

            self.edges_data.append(edge_data)

    def get_nodes(self) -> List[Dict[str, Any]]:
        """
        Get extracted nodes.

        Returns:
            List of node dictionaries with id, label, and properties
        """
        return self.nodes_data

    def get_edges(self) -> List[Dict[str, Any]]:
        """
        Get extracted edges.

        Returns:
            List of edge dictionaries with source_id, target_id, type, and properties
        """
        return self.edges_data

    def get_topology(self) -> Dict[str, Any]:
        """
        Get graph topology information.

        Returns:
            Dictionary containing node labels, relationship types, node count, edge count
        """
        return {
            "node_labels": sorted(list(self.node_labels)),
            "relationship_types": sorted(list(self.relationship_types)),
            "node_count": len(self.nodes_data),
            "edge_count": len(self.edges_data),
        }

    def get_sample_config(self) -> Dict[str, Any]:
        """
        Generate a sample migration configuration template.

        Returns:
            Configuration dictionary for customising label and property mappings
        """
        config = {
            "node_labels": {
                label: {"target_label": label, "property_mappings": {}}
                for label in self.node_labels
            },
            "relationship_types": {
                rel_type: {"target_type": rel_type, "property_mappings": {}}
                for rel_type in self.relationship_types
            },
            "property_transformations": {},
        }
        return config

    def save_topology(self, filepath: str) -> None:
        """
        Save topology information to JSON file.

        Args:
            filepath: Path to save topology JSON
        """
        with open(filepath, "w") as f:
            json.dump(self.get_topology(), f, indent=2)

    def save_sample_config(self, filepath: str) -> None:
        """
        Save sample configuration template to JSON file.

        Args:
            filepath: Path to save sample config JSON
        """
        with open(filepath, "w") as f:
            json.dump(self.get_sample_config(), f, indent=2)
