from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from routers import auth, users, documents, query
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="OmniRAG Platform",
    description="Intelligent Multi-Agent Knowledge Platform",
    version="1.0.0"
)

# Allow the React frontend (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(documents.router)
app.include_router(query.router)

@app.get("/")
def home():
    return {
        "message": "OmniRAG Platform — Aditya Giri",
        "module": "Platform & Orchestration",
        "status": "running"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}