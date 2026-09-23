from pathlib import Path
from collections.abc import Iterator
from pydantic import BaseModel

def iter_doc_files(path: Path, suffixes: set[str]) -> Iterator[Path]:
    for item in path.rglob("*"):
        if ".git" in item.parts or not item.is_file() or item.suffix not in suffixes:
            continue

        yield item

def chunk_text(text: str, chunk_size: int, overlap: int) -> Iterator[str]:
    if chunk_size < overlap:
        raise ValueError("chunk_size must be greater than overlap")

    step = chunk_size - overlap
    for i in range(0, len(text), step):
        yield text[i:i+chunk_size]

class DocChunk(BaseModel):
    text: str
    source: Path
    chunk_index: int

# TODO: Add streaming of file reading for large files
def iter_chunks(root: Path, suffixes: set[str], chunk_size: int, overlap: int, encoders: list = ["utf-8", "cp1252"]) -> Iterator[DocChunk]:
    i = 0
    for file_path in iter_doc_files(root, suffixes):
        print(f"No: {i}\nReading: {file_path}")
        for encoder in encoders:
            with open(file_path, "r", encoding=encoder) as f:
                try: 
                    content = f.read()
                    for j, text in enumerate(chunk_text(content, chunk_size, overlap)):
                        yield DocChunk(text=text, chunk_index=j, source=file_path)
                    break
                except UnicodeDecodeError as e: 
                    print(f"file: {file_path}\nerror: {e}")
                    continue




if __name__ == "__main__":
    p = Path("data/augury")
    iter_chunks(p, {".md", ".txt", ".rst"}, 1000, 150)