"""CLI entry point for PageIndex."""

import argparse
import asyncio
import sys
from pathlib import Path
from .page_index import build_document_index
from .storage import IndexStorage
from .utils import print_tree


def main() -> int:
    parser = argparse.ArgumentParser(description="PageIndex: Document Index for Vectorless RAG")
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument("--storage", default="./index_store", help="Storage directory")
    parser.add_argument("--title", default="", help="Document title")
    parser.add_argument("--doc-id", default="", help="Document ID")
    parser.add_argument("--print-tree", action="store_true", help="Print document tree")
    parser.add_argument("--list", action="store_true", help="List stored indexes")

    args = parser.parse_args()

    storage = IndexStorage(args.storage)

    if args.list:
        indexes = storage.list_indexes()
        if indexes:
            print("Stored indexes:")
            for idx in indexes:
                print(f"  {idx}")
        else:
            print("No indexes found")
        return 0

    if not Path(args.pdf_path).exists():
        print(f"Error: File not found: {args.pdf_path}")
        return 1

    doc_id = args.doc_id or None
    index = asyncio.run(build_document_index(
        args.pdf_path,
        title=args.title,
        doc_id=doc_id,
        storage=storage,
    ))

    print(f"Indexed document: {index.title} (ID: {index.doc_id})")
    print(f"Pages: {index.total_pages}")
    print(f"Version: {index.version}")

    if args.print_tree:
        print("\nDocument structure:")
        print_tree(index.structure)

    return 0


if __name__ == "__main__":
    sys.exit(main())
</arg_key>
<arg_key=i</arg_key>
<arg_value>Create CLI module
