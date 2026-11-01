"""
PageIndex: Document Index for Vectorless, Reasoning-based RAG
"""

from .page_index import build_document_index, add_page_offset_to_toc_json, update_document_index, compute_content_hash
from .storage import IndexStorage
from .utils import list_to_tree, get_leaf_nodes, is_leaf_node, format_structure, print_tree
from .models import DocumentIndex, DocumentNode, PageContent

__version__ = "0.1.0"

__all__ = [
    "build_document_index",
    "add_page_offset_to_toc_json",
    "update_document_index",
    "compute_content_hash",
    "IndexStorage",
    "list_to_tree",
    "get_leaf_nodes",
    "is_leaf_node",
    "format_structure",
    "print_tree",
    "DocumentIndex",
    "DocumentNode",
    "PageContent",
]
