from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

load_dotenv()

template = """Answer the question using only the context below.
If the context doesn't contain the answer, say you don't know.

Context:
{context}

Question:
{question}
"""


model = init_chat_model("gpt-4o-mini", model_provider="openai")

parser = StrOutputParser()

# Normal Prompt
prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model | parser

# Validation prompt
grading_template = """Question: {question}
Answer: {answer}

Does the Answer directly and correctly address the question? Reply with only "yes" or "no".
"""

grading_prompt = ChatPromptTemplate.from_template(grading_template)
grading_chain = grading_prompt | model | parser

if __name__ == "__main__":
    print(chain.invoke({"context": "my name is lakhan", "question": "who is shyam"}))