"""
Improved VectorDB Handling
"""
import os
from typing import List, Any, Callable, Dict

from chromadb.api import Embeddings
from langchain.schema import Document
from langchain.vectorstores import Chroma

def hash_doc_metadata(doc: Document):
    """
    Default hash method, create a hash
    of the document based upon its metadata

    Args:
        doc:

    Returns:

    """
    return hash_metadata(doc.metadata)

def hash_metadata(metadata: Dict):
    return hash(tuple(metadata.items()))

class LocalChromaStore(Chroma):
    existing_docs: set

    def __init__(self, *args, **kwargs):
        self.existing_docs = set()
        super().__init__(*args, **kwargs)
    @classmethod
    def connect(cls,
                persist_dir: str,
                embedding_model: Embeddings) -> 'LocalChromaStore':
        """
        Connect to a local Chroma db.

        If the directory exists, load it. If it does not, create a new one.

        Args:
            persist_dir: Directory to persist
            embedding_model: Model for which embeddings will be created

        Returns:
            The Chroma Store
        """
        if not os.path.exists(persist_dir):
            os.makedirs(persist_dir)

        return cls(persist_directory=persist_dir,
                   embedding_function=embedding_model)

    def in_collection(self, document: Document,
                      unique_key: Callable = None):
        unique_key = unique_key or hash_doc_metadata
        return unique_key(document) in self.existing_docs
    def add_documents(self, documents: List[Document],
                      skip_existing: bool = True,
                      unique_key: Callable = None,
                      **kwargs: Any) -> List[str]:
        """
        Add documents to the vector store.

        If skip_existing is true, don't generate embeddings for documents that
        already exist.

        Args:
            documents: List of documents to add embeddings for.
            skip_existing: If true, don't generate new embeddings for existing docs.
            unique_key: Function to determine how a document's identity
            **kwargs:

        Returns:

        """
        # The default key function is to hash the document's metadata
        unique_key = unique_key or hash_doc_metadata

        if skip_existing:
            documents = [doc for doc in documents
                         if unique_key(doc) not in self.existing_docs]

        # Only try to add documents if the list is not empty.
        if documents:
            super().add_documents(documents, **kwargs)
            self.existing_docs |= {unique_key(doc) for doc in documents}

    def delete_collection(self) -> None:
        self.existing_docs = set()
        super().delete_collection()

