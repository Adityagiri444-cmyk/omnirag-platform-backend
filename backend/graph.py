from typing import TypedDict
from langgraph.graph import StateGraph, END
from nodes import node_retrieval, node_summarizer, node_evaluator, route_after_evaluator

class GraphState(TypedDict):
    query: str
    retrieved_docs: list
    final_answer: str
    evaluation: str
    attempts: int

builder = StateGraph(GraphState)
builder.add_node("retrieval", node_retrieval)
builder.add_node("summarizer", node_summarizer)
builder.add_node("evaluator", node_evaluator)

builder.set_entry_point("retrieval")
builder.add_edge("retrieval", "summarizer")
builder.add_edge("summarizer", "evaluator")

builder.add_conditional_edges(
    "evaluator",
    route_after_evaluator,
    {
        "retry": "retrieval",
        "done": END
    }
)

graph = builder.compile()

if __name__ == "__main__":
    result = graph.invoke({"query": "What is RAG?", "attempts": 0})
    print("Final Answer:\n", result["final_answer"])
    print("\nEvaluation:", result["evaluation"])
    print("Attempts:", result["attempts"])