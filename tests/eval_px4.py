import asyncio
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, context_precision, context_recall, answer_relevancy
from pydantic import BaseModel
from pprint import pprint

from augury.utils.load_json import load_json
from augury.rag.agent import build_agents, RAGState
from augury.rag.embed import LocalEmbedder
from augury.storage.store import VectorStore

class Fixture(BaseModel):
    question: str
    ground_truth: str

async def test():
    data = load_json("tests/fixtures/px4_eval_questions.json")

    e = LocalEmbedder()
    s = VectorStore(e, path="data/chroma")
    agent = build_agents(s)

    answer: list[str] = []
    contexts: list[list[str]] = []
    for question_groundtruth in data:
        ask: RAGState = {
            'context': [],
            "answer": "",
            "is_good": False,
            "attempts": 0,
            "question": question_groundtruth["question"]
        }

        response: RAGState = await agent.ainvoke(ask)

        answer.append(response["answer"])
        contexts.append(response["context"])

    dataset_schema = {
        "question": [val["question"] for val in data],
        "answer": answer,
        "contexts": contexts,
        "ground_truth": [val["ground_truth"] for val in data]
    }
    pprint(dataset_schema)
    dataset = Dataset.from_dict(dataset_schema)

    # Answer ↔ Context → faithfulness
    # Ground truth ↔ Context → context recall
    # Question ↔ Context → context precision
    # Question ↔ Answer → answer relevancy
    results = evaluate(dataset, metrics=[faithfulness, context_recall, context_precision, answer_relevancy])

    pprint(results)

if __name__ == "__main__":
    asyncio.run(test())