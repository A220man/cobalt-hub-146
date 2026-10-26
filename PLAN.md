# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

core-indexing

## Roadmap

### core-indexing — Core Document Indexing Pipeline

Status: in_progress

Acceptance:
- Parse PDF documents and extract text content
- Build hierarchical tree structure from document content
- Store index with document metadata and structure
- Query indexed documents with basic retrieval

### incremental-updates — Incremental Index Updates for Large Documents

Status: planned

Acceptance:
- Detect changed sections between document versions
- Rebuild only affected branches of the document tree
- Recompute summaries only along impacted paths

### usage-observability — Per-Call Chat Usage Observability

Status: planned

Acceptance:
- Expose individual model-call usage records
- Distinguish complete, partial, and unknown measurements
- Preserve cache-read, cache-write, and reasoning quantities

### leaf-nodes-bugfix — Fix get_leaf_nodes KeyError Bug

Status: planned

Acceptance:
- get_leaf_nodes handles nodes without 'nodes' key
- Returns leaf nodes correctly from tree built by list_to_tree

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

Status: planned

Acceptance:
- Handle None page values in add_page_offset_to_toc_json
- Process TOC with missing page numbers gracefully

