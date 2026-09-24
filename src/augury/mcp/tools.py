from pydantic import BaseModel
from pathlib import Path

from augury.storage.store import VectorStore
from augury.rag.embed import LocalEmbedder

e = LocalEmbedder()
s = VectorStore(e, path="data/chroma")

class SearchResult(BaseModel): 
    text: str
    source: Path
    chunk_index: int

def search_docs(query: str) -> list[SearchResult]:
    """Search the Augury technical documentation for relevant information about 
    ArduPilot and PX4. Use this tool when answering questions that require 
    information from the indexed documentation. 
    
    Returns matching documentation chunks with their source and chunk index.
    """
    response = s.query(query=query)

    search_results: list[SearchResult] = [
        SearchResult(
            text=doc_chunk.text,
            source=doc_chunk.source,
            chunk_index=doc_chunk.chunk_index
        ) for doc_chunk in response
    ]

    return search_results