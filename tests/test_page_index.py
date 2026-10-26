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
</arg_key>
<arg_key=i</arg_key>
<arg_value>Create test page_index module
