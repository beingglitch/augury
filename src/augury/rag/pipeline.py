from pathlib import Path

from augury.storage.store import VectorStore
from augury.rag.embed import LocalEmbedder
from augury.rag.ingest import DocChunk, iter_chunks
from augury.rag.chain import chain

def answer_question(question: str) -> str:
    e = LocalEmbedder()
    s = VectorStore(e)

    # Retrieval
    doc_chunks: list[DocChunk] = s.query(query=question)

    # Augmentation
    context = ""
    for chunk in doc_chunks:
        context += " " + chunk.text
    new_input = {"context": context, "question": question}

    # Generation
    answer = chain.invoke(new_input)

    return answer


def index_documents(root: Path, suffixes: set[str], batch_size: int = 128):
    e = LocalEmbedder()
    s = VectorStore(e)

    # Get Chunk Traversal Iterator
    chunks = iter_chunks(root, suffixes, 1024, 128)

    batch = []
    for chunk in chunks:
        batch.append(chunk)

        if len(batch) == batch_size:
            s.add(list(batch))
            batch = []

    # Covering remaining elements
    if batch:
        s.add(list(batch))