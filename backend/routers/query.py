import uuid
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from models import User
from dependencies import get_current_user
from graph import graph

router = APIRouter(prefix="/query", tags=["Query"])

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    evaluation: str
    attempts: int

# In-memory task status store (fine for single-user local dev, not production-scale)
task_status: dict = {}

def run_graph_task(task_id: str, question: str):
    task_status[task_id] = {
        "current_step": "starting",
        "completed_steps": [],
        "done": False,
        "answer": None,
        "evaluation": None,
        "attempts": None,
        "error": None,
    }
    state = {"query": question, "attempts": 0}
    try:
        for step_output in graph.stream(state):
            node_name = list(step_output.keys())[0]
            node_update = step_output[node_name]
            state.update(node_update)
            task_status[task_id]["current_step"] = node_name
            task_status[task_id]["completed_steps"].append(node_name)

        task_status[task_id]["done"] = True
        task_status[task_id]["current_step"] = None
        task_status[task_id]["answer"] = state.get("final_answer")
        task_status[task_id]["evaluation"] = state.get("evaluation")
        task_status[task_id]["attempts"] = state.get("attempts")
    except Exception as e:
        task_status[task_id]["done"] = True
        task_status[task_id]["error"] = str(e)

@router.post("/", response_model=QueryResponse)
def run_query(
    request: QueryRequest,
    current_user: User = Depends(get_current_user)
):
    result = graph.invoke({"query": request.question, "attempts": 0})
    return {
        "answer": result["final_answer"],
        "evaluation": result["evaluation"],
        "attempts": result["attempts"]
    }

@router.post("/start")
def start_query(
    request: QueryRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    task_id = str(uuid.uuid4())
    background_tasks.add_task(run_graph_task, task_id, request.question)
    return {"task_id": task_id}

@router.get("/status/{task_id}")
def get_query_status(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    status = task_status.get(task_id)
    if not status:
        raise HTTPException(status_code=404, detail="Task not found")
    return status