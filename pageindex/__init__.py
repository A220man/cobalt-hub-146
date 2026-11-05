"""
PageIndex: Document Index for Vectorless, Reasoning-based RAG
"""

from .models import DocumentIndex, DocumentNode, PageContent
from .page_index import (
    add_page_offset_to_toc_json,
    build_document_index,
    compute_content_hash,
    update_document_index,
)
from .storage import IndexStorage
from .utils import format_structure, get_leaf_nodes, is_leaf_node, list_to_tree, print_tree

__version__ = "0.1.0"

__all__ = [
    "DocumentIndex",
    "DocumentNode",
    "IndexStorage",
    "PageContent",
    "add_page_offset_to_toc_json",
    "build_document_index",
    "compute_content_hash",
    "format_structure",
    "get_leaf_nodes",
    "is_leaf_node",
    "list_to_tree",
    "print_tree",
    "update_document_index",
]
