import chromadb

from augury.rag.ingest import DocChunk
from augury.rag.embed import Embedder

class VectorStore:
    def __init__(self, embedder: Embedder, name: str = "augury_docs", path: str = "/data/chroma"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(name=name)
        self.embedder = embedder

    # Ingestion
    def add(self, chunks: list[DocChunk]):
        chunks_text = [chunk.text for chunk in chunks]

        embedded_chunks = self.embedder.embed(chunks_text)
        self.collection.add(
            embeddings=embedded_chunks, 
            metadatas=[
                { 
                    "source": str(chunk.source), 
                    "chunk_index": chunk.chunk_index
                } 
                for chunk in chunks
            ],
            ids=[f"{chunk.source}:{chunk.chunk_index}" for chunk in chunks],
            documents=chunks_text
        )

    # Retrieval
    def query(self, query: str, n_results: int = 5) -> list[DocChunk]:
        embedded_query = self.embedder.embed([query])

        data = self.collection.query(query_embeddings=embedded_query, n_results=n_results)

        return [
            DocChunk(text=i[0], source=i[1]["source"], chunk_index=i[1]["chunk_index"])
            for i in zip(data["documents"][0], data["metadatas"][0])
            ]

if __name__ == "__main__":
    from augury.rag.ingest import iter_chunks
    from pathlib import Path
    from augury.rag.embed import LocalEmbedder

    chunks = list(iter_chunks(Path("data/poems"), {".txt"}, 1028, 32))

    s = VectorStore(LocalEmbedder)

    # s.add(chunks)
    # print(s.collection.count())

    print(s.query("who is author"))