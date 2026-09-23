import pytest

from augury.rag.embed import LocalEmbedder

@pytest.mark.parametrize("lists", [
    (["hellow rold"]),
    (["hellow", "world"])
])
def test_local_embedder(lists):
    e = LocalEmbedder()
    output = e.embed(lists)

    # output should be not null
    length = len(output)
    assert length > 0

    # Checking type
    assert isinstance(output, list)

    # Checking size
    assert len(output) == len(lists)

    # Checking inner lists
    l_length = len(output[0])
    for l in output:
        assert len(l) == l_length
        assert isinstance(l, list)
        for n in l:
            assert isinstance(n, float)
    