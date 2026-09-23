from typing import Protocol
from sentence_transformers import SentenceTransformer
from openai import OpenAI

class Embedder(Protocol):
    def embed(self, texts: list[str]) -> list[list[float]]:
        ...

class LocalEmbedder:
    def __init__(self, model_name="BAAI/bge-base-en-v1.5"):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: list[str]) -> list[list[float]]:
        vectors = self.model.encode(texts)
        return vectors.tolist()

class OpenAIEmbedder:
    def __init__(self, model="text-embedding-3-small"):
        self.client = OpenAI()
        self.model = model

    def embed(self, texts: list[str]) -> list[list[float]]:
        print(self.client.embeddings.create(input=texts, model=self.model))
        # TODO: return list[list[str]]
    
if __name__=="__main__":
    # e = LocalEmbedder()
    # print(e.embed(["Hellow rold"]))

    e = OpenAIEmbedder()
    print(e.embed(["Hellow rold"]))
