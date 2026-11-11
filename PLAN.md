# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

incremental-updates

## Roadmap

### core-indexing — Core Document Indexing Pipeline

Status: done

Acceptance:
- Parse PDF documents and extract text content
- Build hierarchical tree structure from document content
- Store index with document metadata and structure
- Query indexed documents with basic retrieval

Implementation: `pageindex/page_index.py`, `pageindex/pdf_extract.py`, `pageindex/utils.py`, `pageindex/storage.py`, `pageindex/models.py`, `pageindex/cli.py`

Tests: `tests/test_page_index.py`, `tests/test_utils.py`

### incremental-updates — Incremental Index Updates for Large Documents

Status: done

Acceptance:
- Detect changed sections between document versions
- Rebuild only affected branches of the document tree
- Recompute summaries only along impacted paths (requires LLM integration; tracked separately)

Implementation: `pageindex/page_index.py`

Tests: `tests/test_page_index.py::test_merge_tree_structures_unchanged_leaf`, `tests/test_page_index.py::test_merge_tree_structures_changed_leaf`, `tests/test_page_index.py::test_merge_tree_structures_nested`

### usage-observability — Per-Call Chat Usage Observability

Status: planned

Acceptance:
- Expose individual model-call usage records
- Distinguish complete, partial, and unknown measurements
- Preserve cache-read, cache-write, and reasoning quantities

### leaf-nodes-bugfix — Fix get_leaf_nodes KeyError Bug

Status: done

Acceptance:
- get_leaf_nodes handles nodes without 'nodes' key
- Returns leaf nodes correctly from tree built by list_to_tree

Implementation: `pageindex/utils.py`

Tests: `tests/test_utils.py::test_get_leaf_nodes_no_keyerror`

### mcp-server — Standalone Local MCP Server

Status: planned

Acceptance:
- stdio transport MCP server exposing agent tools
- pageindex-mcp console entry point
- Integration with PageIndexLocalClient

### pydantic-validation — Pydantic Validation for LLM JSON Outputs

Status: planned

Acceptance:
- Schema validation for LLM responses in indexing pipeline
- Fail deterministically on malformed JSON

### toc-page-offset-bugfix — Fix TOC Page Offset NoneType Error

Status: done

Acceptance:
- Handle None page values in add_page_offset_to_toc_json
- Process TOC with missing page numbers gracefully

Implementation: `pageindex/page_index.py`

Tests: `tests/test_page_index.py::test_add_page_offset_to_toc_json_none_page`

