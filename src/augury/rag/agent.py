from typing import TypedDict
from langgraph.graph import StateGraph, END
import asyncio

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

    async def generate(state: RAGState):

        new_answer = await chain.ainvoke({ 'context': state['context'], 'question': state['question']})

        return {'answer': new_answer}

    async def grade(state: RAGState):
        response = await grading_chain.ainvoke({'question': state['question'], 'answer': state['answer']})
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
    async def main():
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
    
        result = await app.ainvoke(ask)
    
        print(result)

    asyncio.run(main())