from typing import TypedDict
from langgraph.graph import StateGraph, END

from augury.storage.store import VectorStore
from augury.rag.embed import LocalEmbedder
from augury.rag.chain import chain, grading_chain

class RAGState(TypedDict):
    question: str
    answer: str
    context: str
    is_good: bool
    attempts: int

MAX_ATTEMPTS = 5

# Build Agent resolve issue of building embedder and store in every retrieval
def build_agents(store: VectorStore):
    def retrieve(state: RAGState):
        # e = LocalEmbedder()
        # store = VectorStore(e, path="data/chroma")

        chunks = store.query(query=state['question'], n_results=10)

        new_context = ""
        for chunk in chunks:
            new_context += " " + chunk.text

        return {'context': new_context}

    def generate(state: RAGState):

        new_answer = chain.invoke({ 'context': state['context'], 'question': state['question']})

        return {'answer': new_answer}

    def grade(state: RAGState):
        response = grading_chain.invoke({'question': state['question'], 'answer': state['answer']})
        is_good = response.strip().lower() == 'yes'

        return {'is_good': is_good, 'attempts': state["attempts"] + 1}

    def route(state: RAGState) -> str: 
        if state["is_good"] or state["attempts"] >= MAX_ATTEMPTS:
            return END

        return 'retrieve'


    graph = StateGraph(RAGState)

    # Nodes
    graph.add_node("retrieve", retrieve)
    graph.add_node("generate", generate)
    graph.add_node("grade", grade)

    # Edges
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", "grade")

    graph.add_conditional_edges("grade", route)

    # Entry Node
    graph.set_entry_point('retrieve')

    return graph.compile()

if __name__ == "__main__":
    e = LocalEmbedder()
    store = VectorStore(e, path="data/chroma")

    app = build_agents(store)

    ask: RAGState = {
        'context': "",
        "answer": "",
        "is_good": False,
        "attempts": 0,
        "question": "what is hexacopter"
    }

    result = app.invoke(ask)

    print(result)