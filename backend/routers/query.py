from fastapi import APIRouter, Depends
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
