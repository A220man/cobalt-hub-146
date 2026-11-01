# Changelog

## 1.1.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.0.0 — 2026-11-01

### Core Document Indexing Pipeline

- PDF text extraction via pdfplumber
- Hierarchical tree building from TOC/structure
- Content hashing for leaf nodes (foundation for incremental updates)
- JSON storage with document metadata
- CLI with index, list, and tree-print commands

### Bug Fixes

- **Issue #330**: Fixed `get_leaf_nodes` KeyError on leaf nodes (missing `nodes` key)
- **Issue #153**: Fixed `add_page_offset_to_toc_json` TypeError when page is missing

### Testing

- Added `tests/test_utils.py` with 4 tests covering tree building, leaf node extraction, and formatting
- Added `tests/test_page_index.py` with 2 tests verifying TOC page offset handling
- All 6 tests pass

## 0.0.0 — Initial scaffold

Partial code published for continued development.
