import pytest

from augury.rag.ingest import chunk_text

@pytest.mark.parametrize("text, chunk_size, overlap, expected",[
    ("helloworld", 5, 2, ["hello", "lowor", "orld", "d"]),
    ("helloworldef", 5, 2, ["hello", "lowor", "orlde", "def"])
])
def test_chunk_text(text, chunk_size, overlap, expected):
    result = list(chunk_text(text, chunk_size, overlap))
    assert result == expected