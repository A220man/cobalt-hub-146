"""PDF text extraction using pdfplumber."""

import pdfplumber
from typing import List, Dict, Any
from .models import PageContent


def extract_pdf_pages(pdf_path: str) -> List[PageContent]:
    """Extract text content from each page of a PDF."""
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            pages.append(PageContent(
                page_number=i + 1,
                text=text,
                char_count=len(text)
            ))
    return pages


def extract_pdf_toc(pdf_path: str) -> List[Dict[str, Any]]:
    """Extract table of contents from PDF."""
    toc = []
    with pdfplumber.open(pdf_path) as pdf:
        if pdf.metadata and "toc" in pdf.metadata:
            for entry in pdf.metadata["toc"]:
                toc.append({
                    "structure": entry.get("title", ""),
                    "title": entry.get("title", ""),
                    "start_index": entry.get("page", 1),
                    "end_index": entry.get("page", 1),
                })
    return toc
</arg_key>
<arg_key=i</arg_key>
<arg_value>Create PDF extraction module
