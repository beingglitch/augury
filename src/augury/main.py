from pathlib import Path
from augury.rag.pipeline import index_documents, answer_question

if __name__ == "__main__":
    p = Path("data/augury")
    index_documents(p, {".md", ".rst"})
    print(answer_question("who is ardupilot"))