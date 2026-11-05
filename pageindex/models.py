from typing import Any

from pydantic import BaseModel, Field


class DocumentNode(BaseModel):
    """A node in the document hierarchy tree."""
    structure: str = Field(..., description="Section number like 1.2.3")
    title: str = Field(..., description="Section title")
    start_index: int = Field(..., description="Start page (1-based)")
    end_index: int = Field(..., description="End page (1-based)")
    nodes: list["DocumentNode"] = Field(default_factory=list, description="Child nodes")
    summary: str | None = Field(default=None, description="Generated summary")
    content_hash: str | None = Field(default=None, description="Hash for incremental updates")


class DocumentIndex(BaseModel):
    """Complete document index."""
    doc_id: str = Field(..., description="Unique document identifier")
    title: str = Field(..., description="Document title")
    total_pages: int = Field(..., description="Total page count")
    structure: DocumentNode = Field(..., description="Root of document hierarchy")
    pages: list["PageContent"] = Field(default_factory=list, description="Page contents")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    version: int = Field(default=1, description="Index version for incremental updates")


class PageContent(BaseModel):
    """Content of a single page."""
    page_number: int = Field(..., description="1-based page number")
    text: str = Field(..., description="Extracted text content")
    char_count: int = Field(..., description="Character count")


# Forward reference resolution
DocumentNode.model_rebuild()
DocumentIndex.model_rebuild()
