"""Utility functions for tree operations and formatting."""

import copy
from typing import Any, Dict, List


def clean_node(node: Dict[str, Any]) -> None:
    """Remove empty nodes key from leaf nodes."""
    if not node.get("nodes"):
        node.pop("nodes", None)


def list_to_tree(flat_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Convert flat list of sections to hierarchical tree."""
    if not flat_list:
        return {}

    # Build tree from flat list
    root = {"nodes": []}
    stack = [(0, root)]  # (level, parent_node)

    for item in flat_list:
        level = item["structure"].count(".")
        node = {
            "structure": item["structure"],
            "title": item["title"],
            "start_index": item["start_index"],
            "end_index": item["end_index"],
            "nodes": [],
        }

        # Find parent
        while stack and stack[-1][0] >= level:
            stack.pop()

        parent = stack[-1][1]
        parent["nodes"].append(node)
        stack.append((level, node))

    # Clean up empty nodes
    def clean_recursive(n: Dict[str, Any]) -> None:
        for child in n.get("nodes", []):
            clean_recursive(child)
        clean_node(n)

    clean_recursive(root)
    return root["nodes"][0] if root["nodes"] else {}


def get_leaf_nodes(structure: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get all leaf nodes from tree structure."""
    if isinstance(structure, dict):
        if not structure.get("nodes"):  # Fixed: use .get() to handle missing key
            structure_node = copy.deepcopy(structure)
            structure_node.pop("nodes", None)
            return [structure_node]
        else:
            leaf_nodes = []
            for key in list(structure.keys()):
                if "nodes" in key:
                    leaf_nodes.extend(get_leaf_nodes(structure[key]))
            return leaf_nodes
    return []


def is_leaf_node(structure: Dict[str, Any]) -> bool:
    """Check if a node is a leaf (has no children)."""
    return not structure.get("nodes")


def format_structure(structure: Dict[str, Any], indent: int = 0) -> str:
    """Format tree structure as string."""
    lines = []
    prefix = "  " * indent
    lines.append(f"{prefix}{structure.get('structure', '')} {structure.get('title', '')}")
    for child in structure.get("nodes", []):
        lines.append(format_structure(child, indent + 1))
    return "\n".join(lines)


def print_tree(structure: Dict[str, Any], indent: int = 0) -> None:
    """Print tree structure to stdout."""
    print(format_structure(structure, indent))
</arg_key>
<arg_key=i</arg_key>
<arg_value>Create utils with fixed get_leaf_nodes