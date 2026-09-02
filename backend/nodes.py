from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from retriever import retrieve

model = ChatGroq(model="openai/gpt-oss-20b")
parser = StrOutputParser()

summarizer_prompt = PromptTemplate.from_template(
    "Answer the question using only the context below. "
    "If the context doesn't contain the answer, say so.\n\n"
    "Context:\n{context}\n\n"
    "Question: {question}\n\n"
    "Answer:"
)
summarizer_chain = summarizer_prompt | model | parser

def node_summarizer(state: dict) -> dict:
    context = "\n\n".join(state["retrieved_docs"])
    answer = summarizer_chain.invoke({"context": context, "question": state["query"]})
    return {"final_answer": answer}

def node_retrieval(state: dict) -> dict:
    docs = retrieve(state["query"], k=3)
    return {"retrieved_docs": docs}

if __name__ == "__main__":
    test_state = {"query": "What is RAG?"}
    test_state.update(node_retrieval(test_state))
    test_state.update(node_summarizer(test_state))
    print("Final Answer:\n", test_state["final_answer"])