"""Local JSON storage for document indexes."""

import json
from pathlib import Path
from typing import List, Optional
from .models import DocumentIndex


class IndexStorage:
    """Manage document index storage."""

    def __init__(self, storage_path: str):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _index_file(self, doc_id: str) -> Path:
        return self.storage_path / f"{doc_id}.json"

    def save(self, index: DocumentIndex) -> None:
        """Save index to storage."""
        file_path = self._index_file(index.doc_id)
        with open(file_path, "w") as f:
            json.dump(index.model_dump(), f, indent=2)

    def load(self, doc_id: str) -> Optional[DocumentIndex]:
        """Load index from storage."""
        file_path = self._index_file(doc_id)
        if not file_path.exists():
            return None
        with open(file_path) as f:
            data = json.load(f)
        return DocumentIndex.model_validate(data)

    def exists(self, doc_id: str) -> bool:
        return self._index_file(doc_id).exists()

    def list_indexes(self) -> List[str]:
        return [f.stem for f in self.storage_path.glob("*.json")]
