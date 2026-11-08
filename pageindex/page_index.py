"""Main document index building pipeline."""

import hashlib
import uuid
from typing import Any

from .models import DocumentIndex
from .pdf_extract import extract_pdf_pages, extract_pdf_toc
from .storage import IndexStorage
from .utils import get_leaf_nodes, list_to_tree


def compute_content_hash(text: str) -> str:
    """Compute SHA256 hash of content for incremental updates."""
    return hashlib.sha256(text.encode()).hexdigest()[:16]


async def build_document_index(
    pdf_path: str,
    title: str = "",
    doc_id: str | None = None,
    storage: IndexStorage | None = None,
) -> DocumentIndex:
    """Build document index from PDF."""
    if doc_id is None:
        doc_id = str(uuid.uuid4())[:8]

    if not title:
        title = pdf_path.split("/")[-1].replace(".pdf", "")

    # Extract pages
    pages = extract_pdf_pages(pdf_path)

    # Extract TOC
    toc = extract_pdf_toc(pdf_path)

    # If no TOC found, create flat structure from pages
    if not toc:
        toc = [
            {
                "structure": str(i + 1),
                "title": f"Page {i + 1}",
                "start_index": i + 1,
                "end_index": i + 1,
            }
            for i in range(len(pages))
        ]

    # Build tree structure
    structure = list_to_tree(toc)

    # Compute content hashes for leaf nodes
    leaf_nodes = get_leaf_nodes(structure)
    for leaf in leaf_nodes:
        start = leaf["start_index"] - 1
        end = leaf["end_index"]
        content = "".join(p.text for p in pages[start:end])
        leaf["content_hash"] = compute_content_hash(content)

    # Create index
    index = DocumentIndex(
        doc_id=doc_id,
        title=title,
        total_pages=len(pages),
        structure=structure,  # type: ignore[arg-type]
        pages=pages,
    )

    # Save if storage provided
    if storage:
        storage.save(index)

    return index


def add_page_offset_to_toc_json(toc: list[dict[str, Any]], offset: int) -> list[dict[str, Any]]:
    """Add page offset to TOC entries. Fixed: handle None page values."""
    result = []
    for entry in toc:
        new_entry = entry.copy()
        page = entry.get("page")
        if page is not None:
            new_entry["physical_index"] = page + offset
        else:
            new_entry["physical_index"] = offset + 1
        result.append(new_entry)
    return result


async def update_document_index(
    existing_index: DocumentIndex,
    new_pdf_path: str,
    storage: IndexStorage | None = None,
) -> DocumentIndex:
    """Update document index incrementally by comparing content hashes."""
    # Extract new pages
    new_pages = extract_pdf_pages(new_pdf_path)

    # Extract TOC from new PDF
    new_toc = extract_pdf_toc(new_pdf_path)

    # If no TOC found, create flat structure from pages
    if not new_toc:
        new_toc = [
            {
                "structure": str(i + 1),
                "title": f"Page {i + 1}",
                "start_index": i + 1,
                "end_index": i + 1,
            }
            for i in range(len(new_pages))
        ]

    # Build new tree structure
    new_structure_dict = list_to_tree(new_toc)

    # Compute content hashes for new leaf nodes
    new_leaf_nodes = get_leaf_nodes(new_structure_dict)
    for leaf in new_leaf_nodes:
        start = leaf["start_index"] - 1
        end = leaf["end_index"]
        content = "".join(p.text for p in new_pages[start:end])
        leaf["content_hash"] = compute_content_hash(content)

    # Merge: reuse unchanged nodes from existing index
    merged_structure = merge_tree_structures(
        existing_index.structure.model_dump(),
        new_structure_dict
    )

    # Create updated index
    updated_index = DocumentIndex(
        doc_id=existing_index.doc_id,
        title=existing_index.title,
        total_pages=len(new_pages),
        structure=merged_structure,  # type: ignore[arg-type]
        pages=new_pages,
        version=existing_index.version + 1,
    )

    # Save if storage provided
    if storage:
        storage.save(updated_index)

    return updated_index


def merge_tree_structures(
    old_structure: dict[str, Any],
    new_structure: dict[str, Any],
) -> dict[str, Any]:
    """Merge old and new tree structures, reusing unchanged nodes based on content_hash."""
    # If both are leaf nodes, compare content hashes
    old_nodes = old_structure.get("nodes")
    new_nodes = new_structure.get("nodes")

    if not old_nodes and not new_nodes:
        # Both are leaf nodes - compare content hashes
        old_hash = old_structure.get("content_hash")
        new_hash = new_structure.get("content_hash")
        if old_hash == new_hash:
            # Content unchanged - reuse old node (preserves summary, etc.)
            return old_structure
        else:
            # Content changed - use new node
            return new_structure

    # At least one has children - merge recursively
    result = new_structure.copy()
    if new_nodes:
        # Build lookup of old children by structure number
        old_children = {}
        if old_nodes:
            for child in old_nodes:
                old_children[child.get("structure", "")] = child

        merged_children = []
        for new_child in new_nodes:
            structure_key = new_child.get("structure", "")
            old_child = old_children.get(structure_key)
            if old_child:
                # Recursively merge
                merged_child = merge_tree_structures(old_child, new_child)
                merged_children.append(merged_child)
            else:
                # New child - use as-is
                merged_children.append(new_child)
        result["nodes"] = merged_children

    return result
