\# OmniRAG — Intelligent Multi-Agent Knowledge Platform



OmniRAG is a full-stack Retrieval-Augmented Generation (RAG) platform that lets users upload documents, ask questions about them, and get grounded, evaluated answers — with live visualization of the AI's reasoning steps and downloadable PDF reports.



Built as a 5th-semester mini project / TechXpo submission.



\## Features



\- \*\*Authenticated document management\*\* — upload, list, delete, and summarize PDF documents per user, with admin/user role separation

\- \*\*Multi-agent RAG pipeline\*\* (LangGraph): Planner → Retrieval → Summarizer → Evaluator, with automatic retry on ungrounded answers

\- \*\*Real-time agent visualization\*\* — live progress tracking as each pipeline step runs, shown as an animated status bar in the chat UI

\- \*\*Chat interface\*\* — full conversation history, not just single Q\&A

\- \*\*Downloadable PDF reports\*\* — every answer can be exported as a structured report (question, search query, retrieved context, answer, evaluation)

\- \*\*Document summarization\*\* — one-click AI summary of any uploaded document

\- \*\*Analytics dashboard\*\* — upload trends and document counts, visualized with charts



\## Tech Stack



\- \*\*Backend\*\*: FastAPI, SQLAlchemy, SQLite, JWT auth (python-jose), bcrypt

\- \*\*Frontend\*\*: React, Tailwind CSS, Recharts

\- \*\*AI/Orchestration\*\*: LangChain, LangGraph, Groq (free-tier LLM API), HuggingFace sentence-transformers (local embeddings, no API cost)

\- \*\*Vector Store\*\*: ChromaDB (local, persistent)

\- \*\*PDF Processing\*\*: pypdf (extraction), ReportLab (report generation)



\## Architecture



```

User Question

&#x20;    │

&#x20;    ▼

┌─────────┐    ┌───────────┐    ┌────────────┐    ┌───────────┐

│ Planner │───▶│ Retrieval │───▶│ Summarizer │───▶│ Evaluator │

└─────────┘    └───────────┘    └────────────┘    └─────┬─────┘

&#x20;                    ▲                                    │

&#x20;                    └──────────── retry on "NO" ─────────┘

&#x20;                                                           │

&#x20;                                                   (max 2 attempts)

&#x20;                                                           ▼

&#x20;                                                    Final Answer

```



\- \*\*Planner\*\*: rewrites the user's raw question into a focused search query

\- \*\*Retrieval\*\*: finds the most relevant document chunks via vector similarity search

\- \*\*Summarizer\*\*: generates an answer grounded in the retrieved context

\- \*\*Evaluator\*\*: checks whether the answer is actually supported by the context; triggers a retry if not, up to 2 attempts



\## Setup



\### Backend

```bash

cd backend

python -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt

```



Create a `.env` file in `backend/` with:

```

GROQ\_API\_KEY=your\_groq\_api\_key\_here

```

(Get a free key at \[console.groq.com](https://console.groq.com))



Run the server:

```bash

uvicorn main:app --reload

```



\### Frontend

```bash

cd omnirag-frontend

npm install

npm start

```



Opens at `http://localhost:3000`.



\## Usage



1\. Register/log in

2\. Upload PDF documents via "My Documents"

3\. Ask questions in "Ask OmniRAG" — watch the live agent progress bar as it retrieves, generates, and evaluates the answer

4\. Download a PDF report of any answer, or generate a one-paragraph summary of any document



\## Team



\- \*\*Aditya Giri\*\* — Platform Development, Workflow Orchestration, Knowledge Services (FastAPI backend, React frontend, LangGraph orchestration, retrieval engine)

\- \*\*Aryan Patel\*\* — Multi-agent reasoning

\- \*\*Pranjal Agarwal\*\* — Document intelligence (retrieval)

