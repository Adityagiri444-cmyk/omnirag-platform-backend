from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from retriever import retrieve
from retriever import retrieve, get_document_text

model = ChatGroq(model="openai/gpt-oss-20b")
parser = StrOutputParser()

planner_prompt = PromptTemplate.from_template(
    "You are a query planning agent for a document retrieval system. "
    "Given a user's question, rewrite it into the clearest, most specific search query "
    "that will retrieve the most relevant document passages. "
    "If the question has multiple parts, focus on the core information need. "
    "Reply with ONLY the rewritten search query, nothing else.\n\n"
    "User question: {query}\n\n"
    "Search query:"
)
planner_chain = planner_prompt | model | parser

def node_planner(state: dict) -> dict:
    search_query = planner_chain.invoke({"query": state["query"]}).strip()
    return {"search_query": search_query}

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
    query_to_use = state.get("search_query", state["query"])
    docs = retrieve(query_to_use, k=3)
    return {"retrieved_docs": docs}

evaluator_prompt = PromptTemplate.from_template(
    "Question: {question}\n"
    "Context used:\n{context}\n"
    "Generated Answer: {answer}\n\n"
    "Does the answer fully and accurately answer the question using ONLY the context above? "
    "Reply with exactly one word: YES or NO."
)
evaluator_chain = evaluator_prompt | model | parser

def node_evaluator(state: dict) -> dict:
    context = "\n\n".join(state["retrieved_docs"])
    verdict = evaluator_chain.invoke({
        "question": state["query"],
        "context": context,
        "answer": state["final_answer"]
    }).strip().upper()
    attempts = state.get("attempts", 0) + 1
    return {"evaluation": verdict, "attempts": attempts}

def route_after_evaluator(state: dict) -> str:
    if state["evaluation"] == "YES" or state["attempts"] >= 2:
        return "done"
    return "retry"

summary_prompt = PromptTemplate.from_template(
    "Summarize the following document in one clear, well-written paragraph. "
    "Cover the main topic and the most important points.\n\n"
    "Document:\n{text}\n\n"
    "Summary:"
)
summary_chain = summary_prompt | model | parser

def summarize_document(filename: str) -> str:
    text = get_document_text(filename)
    if not text:
        return "No content found for this document."
    text = text[:6000]  # keep within model context limits
    return summary_chain.invoke({"text": text})

if __name__ == "__main__":
    test_state = {"query": "What is RAG?", "attempts": 0}
    test_state.update(node_planner(test_state))
    test_state.update(node_retrieval(test_state))
    test_state.update(node_summarizer(test_state))
    test_state.update(node_evaluator(test_state))
    print("Search Query:", test_state["search_query"])
    print("\nFinal Answer:\n", test_state["final_answer"])
    print("\nEvaluation:", test_state["evaluation"])
    print("Route decision:", route_after_evaluator(test_state))