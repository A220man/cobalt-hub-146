"""Test page_index module - add_page_offset_to_toc_json bug fix (Issue #153)."""

from pageindex.page_index import add_page_offset_to_toc_json


def test_add_page_offset_to_toc_json_none_page():
    """Test handling of None page values (Issue #153)."""
    toc = [
        {"structure": "1", "title": "Chapter 1", "page": None},
        {"structure": "2", "title": "Chapter 2", "page": 3},
    ]
    result = add_page_offset_to_toc_json(toc, 5)
    assert result[0]["physical_index"] == 6  # None -> offset + 1
    assert result[1]["physical_index"] == 8  # 3 + 5


def test_add_page_offset_to_toc_json_all_present():
    """Test normal case with all page values present."""
    toc = [
        {"structure": "1", "title": "Chapter 1", "page": 1},
        {"structure": "2", "title": "Chapter 2", "page": 5},
    ]
    result = add_page_offset_to_toc_json(toc, 10)
    assert result[0]["physical_index"] == 11  # 1 + 10
    assert result[1]["physical_index"] == 15  # 5 + 10

from pageindex.page_index import merge_tree_structures


def test_merge_tree_structures_unchanged_leaf():
    """Test that merge_tree_structures reuses unchanged leaf nodes."""
    old = {
        "structure": "1",
        "title": "Chapter 1",
        "start_index": 1,
        "end_index": 5,
        "content_hash": "abc123",
        "summary": "Original summary",
    }
    new = {
        "structure": "1",
        "title": "Chapter 1",
        "start_index": 1,
        "end_index": 5,
        "content_hash": "abc123",  # Same hash - unchanged
    }
    result = merge_tree_structures(old, new)
    # Should reuse old node (preserves summary)
    assert result["content_hash"] == "abc123"
    assert result["summary"] == "Original summary"


def test_merge_tree_structures_changed_leaf():
    """Test that merge_tree_structures uses new node when content changed."""
    old = {
        "structure": "1",
        "title": "Chapter 1",
        "start_index": 1,
        "end_index": 5,
        "content_hash": "abc123",
        "summary": "Original summary",
    }
    new = {
        "structure": "1",
        "title": "Chapter 1",
        "start_index": 1,
        "end_index": 5,
        "content_hash": "def456",  # Different hash - changed
    }
    result = merge_tree_structures(old, new)
    # Should use new node
    assert result["content_hash"] == "def456"
    # Summary not preserved (new node doesn't have it)
    assert "summary" not in result or result.get("summary") is None


def test_merge_tree_structures_nested():
    """Test recursive merge of nested structures."""
    old = {
        "structure": "",
        "title": "",
        "nodes": [
            {
                "structure": "1",
                "title": "Chapter 1",
                "start_index": 1,
                "end_index": 5,
                "nodes": [
                    {
                        "structure": "1.1",
                        "title": "Section 1.1",
                        "start_index": 1,
                        "end_index": 2,
                        "content_hash": "abc123",
                        "summary": "Old section summary",
                    }
                ],
            },
            {
                "structure": "2",
                "title": "Chapter 2",
                "start_index": 6,
                "end_index": 10,
                "content_hash": "xyz789",
            },
        ],
    }
    new = {
        "structure": "",
        "title": "",
        "nodes": [
            {
                "structure": "1",
                "title": "Chapter 1",
                "start_index": 1,
                "end_index": 5,
                "nodes": [
                    {
                        "structure": "1.1",
                        "title": "Section 1.1",
                        "start_index": 1,
                        "end_index": 2,
                        "content_hash": "abc123",  # Unchanged
                    }
                ],
            },
            {
                "structure": "2",
                "title": "Chapter 2",
                "start_index": 6,
                "end_index": 10,
                "content_hash": "new_hash",  # Changed
            },
        ],
    }
    result = merge_tree_structures(old, new)
    # Chapter 1 Section 1.1 should be reused (unchanged)
    chapter1 = result["nodes"][0]
    section11 = chapter1["nodes"][0]
    assert section11["content_hash"] == "abc123"
    assert section11["summary"] == "Old section summary"
    # Chapter 2 should be new (changed)
    chapter2 = result["nodes"][1]
    assert chapter2["content_hash"] == "new_hash"
