# PageIndex: Document Index for Vectorless, Reasoning-based RAG

> Work in progress. This checkpoint may be incomplete or fail tests. See PLAN.md and STATUS.md before use.


PageIndex builds hierarchical document indexes for vectorless, reasoning-based retrieval-augmented generation (RAG).

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Build index from PDF
pageindex document.pdf --storage ./index_store

# List stored indexes
pageindex --list --storage ./index_store

# Print document tree structure
pageindex document.pdf --print-tree
```

## Development

```bash
# Install with dev dependencies
pip install -e .[dev]

# Run tests
pytest tests/
```

## Bug Fixes Included

- **Issue #330**: Fixed `get_leaf_nodes` KeyError on leaf nodes (missing `nodes` key)
- **Issue #153**: Fixed `add_page_offset_to_toc_json` TypeError with None page values

## License

MIT

Maintainer: Ryan Vo <ryandtvo@gmail.com>
