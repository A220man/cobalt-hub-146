"""Main document index building pipeline."""

import hashlib
import uuid
from typing import List, Dict, Any, Optional
from .models import DocumentIndex, DocumentNode, PageContent
from .utils import list_to_tree, get_leaf_nodes
from .pdf_extract import extract_pdf_pages, extract_pdf_toc
from .storage import IndexStorage


def compute_content_hash(text: str) -> str:
    """Compute SHA256 hash of content for incremental updates."""
    return hashlib.sha256(text.encode()).hexdigest()[:16]


async def build_document_index(
    pdf_path: str,
    title: str = "",
    doc_id: Optional[str] = None,
    storage: Optional[IndexStorage] = None,
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
        structure=structure,
        pages=pages,
    )

    # Save if storage provided
    if storage:
        storage.save(index)

    return index


def add_page_offset_to_toc_json(toc: List[Dict[str, Any]], offset: int) -> List[Dict[str, Any]]:
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
    storage: Optional[IndexStorage] = None,
) -> DocumentIndex:
    """Update document index incrementally (placeholder for full implementation)."""
    # For now, rebuild full index - incremental logic to be implemented
    new_index = await build_document_index(
        new_pdf_path,
        "",
        doc_id=existing_index.doc_id,
        title=existing_index.title,
    )
    new_index.version = existing_index.version + 1
    return new_index
</arg_key>
<arg_key=i</arg_key>
<arg_value>Create page_index.py main module
