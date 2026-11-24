"""Regression test for nodes key consistency in merge_tree_structures.

Issue: When merge_tree_structures receives two leaf node structures with the same
content_hash, it returns old_structure directly. If old_structure has nodes: None
explicitly, the result contains "nodes": null. If old_structure lacks the nodes key
entirely, the result lacks the nodes key. This inconsistency can cause issues for
callers that check for the presence or absence of the nodes key.

This test verifies that the fix normalizes the output consistently.
"""
from pageindex.page_index import merge_tree_structures


def test_merge_tree_structures_nodes_key_consistency_leaf_none_explicit():
    """Test that leaf node with nodes: None explicit normalizes same as no nodes key."""
    old = {"content_hash": "abc123", "title": "Test Section", "nodes": None}
    new = {"content_hash": "abc123", "title": "Test Section"}
    result = merge_tree_structures(old, new)
    # Both cases should result in no "nodes" key
    assert "nodes" not in result, (
        f"Expected no 'nodes' key, but got nodes={result.get('nodes')!r}"
    )


def test_merge_tree_structures_nodes_key_consistency_leaf_no_key():
    """Test that leaf node without nodes key normalizes same as nodes: None."""
    old = {"content_hash": "abc123", "title": "Test Section"}
    new = {"content_hash": "abc123", "title": "Test Section"}
    result = merge_tree_structures(old, new)
    # Both cases should result in no "nodes" key
    assert "nodes" not in result, (
        f"Expected no 'nodes' key, but got nodes={result.get('nodes')!r}"
    )


def test_merge_tree_structures_nodes_key_consistency_both_cases():
    """Test that both explicit nodes: None and absent nodes key produce identical results."""
    old_with_none = {"content_hash": "abc123", "title": "Test Section", "nodes": None}
    old_no_key = {"content_hash": "abc123", "title": "Test Section"}
    new = {"content_hash": "abc123", "title": "Test Section"}

    result_with_none = merge_tree_structures(old_with_none, new)
    result_no_key = merge_tree_structures(old_no_key, new)

    # Both should have the same keys (neither should have "nodes")
    assert set(result_with_none.keys()) == set(result_no_key.keys()), (
        f"Results should have same keys: "
        f"with_none={set(result_with_none.keys())}, "
        f"no_key={set(result_no_key.keys())}"
    )
    # Both should not have "nodes" key
    assert "nodes" not in result_with_none, (
        "Result with nodes: None should not have 'nodes' key after fix"
    )
    assert "nodes" not in result_no_key, (
        "Result without nodes key should not have 'nodes' key after fix"
    )
