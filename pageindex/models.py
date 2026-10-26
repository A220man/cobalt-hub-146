from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class DocumentNode(BaseModel):
    """A node in the document hierarchy tree."""
    structure: str = Field(..., description="Section number like 1.2.3")
    title: str = Field(..., description="Section title")
    start_index: int = Field(..., description="Start page (1-based)")
    end_index: int = Field(..., description="End page (1-based)")
    nodes: List["DocumentNode"] = Field(default_factory=list, description="Child nodes")
    summary: Optional[str] = Field(default=None, description="Generated summary")
    content_hash: Optional[str] = Field(default=None, description="Hash for incremental updates")


class DocumentIndex(BaseModel):
    """Complete document index."""
    doc_id: str = Field(..., description="Unique document identifier")
    title: str = Field(..., description="Document title")
    total_pages: int = Field(..., description="Total page count")
    structure: DocumentNode = Field(..., description="Root of document hierarchy")
    pages: List["PageContent"] = Field(default_factory=list, description="Page contents")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    version: int = Field(default=1, description="Index version for incremental updates")


class PageContent(BaseModel):
    """Content of a single page."""
    page_number: int = Field(..., description="1-based page number")
    text: str = Field(..., description="Extracted text content")
    char_count: int = Field(..., description="Character count")


# Forward reference resolution
DocumentNode.model_rebuild()
DocumentIndex.model_rebuild()
</arg_key>
<arg_key=i</arg_key>
<arg_value>Create data models