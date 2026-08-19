from fastapi import FastAPI
from database import engine
import models
from routers import auth, users          # ← CHANGED: added ", users"

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="OmniRAG Platform",
    description="Intelligent Multi-Agent Knowledge Platform",
    version="1.0.0"
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)          # ← NEW LINE: added this

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