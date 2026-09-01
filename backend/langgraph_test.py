from typing import TypedDict
from langgraph.graph import StateGraph, END

class GraphState(TypedDict):
    input: str
    output: str
    attempts: int

def node_a(state: GraphState) -> GraphState:
    print("Node A running")
    return {"output": f"Processed: {state['input']}", "attempts": state.get("attempts", 0) + 1}

def node_b(state: GraphState) -> GraphState:
    print("Node B running")
    return {"output": state["output"] + " -> checked"}

def route_after_b(state: GraphState) -> str:
    if state["attempts"] < 2:
        return "retry"
    return "done"

builder = StateGraph(GraphState)
builder.add_node("A", node_a)
builder.add_node("B", node_b)
builder.set_entry_point("A")
builder.add_edge("A", "B")

builder.add_conditional_edges(
    "B",
    route_after_b,
    {
        "retry": "A",
        "done": END
    }
)

graph = builder.compile()

result = graph.invoke({"input": "hello", "attempts": 0})
print(result)