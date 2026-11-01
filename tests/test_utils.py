"""Test utils module - get_leaf_nodes bug fix verification."""

import copy
from pageindex.utils import get_leaf_nodes, list_to_tree, is_leaf_node, format_structure


def test_get_leaf_nodes_no_keyerror():
    """Test that get_leaf_nodes handles nodes without 'nodes' key (Issue #330)."""
    flat = [
        {"structure": "1", "title": "Chapter 1", "start_index": 1, "end_index": 5},
        {"structure": "2", "title": "Chapter 2", "start_index": 6, "end_index": 10},
    ]
    tree = list_to_tree(flat)
    # This should not raise KeyError
    leaves = get_leaf_nodes(tree)
    assert len(leaves) == 2
    assert leaves[0]["title"] == "Chapter 1"
    assert leaves[1]["title"] == "Chapter 2"
    # Verify nodes key is not present on leaves
    for leaf in leaves:
        assert "nodes" not in leaf


def test_is_leaf_node():
    flat = [
        {"structure": "1", "title": "Chapter 1", "start_index": 1, "end_index": 5},
        {"structure": "1.1", "title": "Section 1.1", "start_index": 1, "end_index": 2},
        {"structure": "2", "title": "Chapter 2", "start_index": 6, "end_index": 10},
    ]
    tree = list_to_tree(flat)
    # Chapter 1 has children, not leaf
    assert not is_leaf_node(tree)
    # Chapter 2 is leaf
    chapter2 = tree["nodes"][1]
    assert is_leaf_node(chapter2)


def test_format_structure():
    flat = [
        {"structure": "1", "title": "Chapter 1", "start_index": 1, "end_index": 5},
        {"structure": "2", "title": "Chapter 2", "start_index": 6, "end_index": 10},
    ]
    tree = list_to_tree(flat)
    output = format_structure(tree)
    assert "Chapter 1" in output
    assert "Chapter 2" in output


def test_list_to_tree_nested():
    flat = [
        {"structure": "1", "title": "Chapter 1", "start_index": 1, "end_index": 10},
        {"structure": "1.1", "title": "Section 1.1", "start_index": 1, "end_index": 5},
        {"structure": "1.2", "title": "Section 1.2", "start_index": 6, "end_index": 10},
        {"structure": "2", "title": "Chapter 2", "start_index": 11, "end_index": 15},
    ]
    tree = list_to_tree(flat)
    # With multiple top-level items, returns virtual root
    assert tree["structure"] == ""
    assert tree["title"] == ""
    assert len(tree["nodes"]) == 2  # Chapter 1 and Chapter 2
    chapter1 = tree["nodes"][0]
    assert chapter1["title"] == "Chapter 1"
    assert len(chapter1["nodes"]) == 2  # Section 1.1 and Section 1.2
    assert chapter1["nodes"][0]["title"] == "Section 1.1"
    assert chapter1["nodes"][1]["title"] == "Section 1.2"
    chapter2 = tree["nodes"][1]
    # Chapter 2 is a leaf, so 'nodes' key is removed by clean_node
    assert "nodes" not in chapter2
    assert is_leaf_node(chapter2)
