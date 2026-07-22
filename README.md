Here is the streamlined `README.md` with the simplified 2-liner setup section:

```markdown
# 🤖 Support Ticket & Technical Document Triage Agent

A production-grade, agentic RAG system built to triage technical documentation queries and look up customer support tickets dynamically.

---

## 🎯 Project Overview

This flagship system combines **Retrieval-Augmented Generation (RAG)** over technical documentation with **dynamic agent tool-calling**, a **FastAPI backend REST service**, **SQLite telemetry/observability**, and an interactive **Streamlit frontend chat UI**.

### Key Highlights
- **100% Tool Routing Accuracy** across 20 benchmark test cases.
- **0% Tool Hallucination Rate** on casual greetings and out-of-scope queries.
- **6.22s Average Latency** with complete query logging and telemetry.
- **Strict Source Citations** referencing exact documentation files for every RAG query.

---

## 🏗️ System Architecture


```

```
                           ┌─────────────────────────┐
                           │   User (Browser)        │
                           └────────────┬────────────┘
                                        │
                                        ▼ (HTTP POST /chat)
                           ┌─────────────────────────┐
                           │ Streamlit UI (app.py)   │
                           └────────────┬────────────┘
                                        │
                                        ▼
                           ┌─────────────────────────┐
                           │ FastAPI Backend         │
                           │ (main.py + SQLite Log)  │
                           └────────────┬────────────┘
                                        │
                                        ▼
                           ┌─────────────────────────┐
                           │  LangChain Agent Engine │
                           │       (agent.py)        │
                           └───────┬───────────┬─────┘
                                   │           │
       ┌───────────────────────────┘           └───────────────────────────┐
       ▼                                                                   ▼

```

┌───────────────────────────────┐                           ┌──────────────────────────────────┐
│ Tool: search_fastapi_docs     │                           │ Tool: check_ticket_status        │
│ (ChromaDB Vector Store)       │                           │ (Mock Ticket Database)           │
└───────────────────────────────┘                           └──────────────────────────────────┘

```

---

## 🛠️ Tech Stack & Key Components

| Component | Technology | Description |
| :--- | :--- | :--- |
| **LLM Model** | `gemini-3.1-flash-lite` | Zero-temperature model via Google AI Studio API |
| **Embeddings** | `gemini-embedding-001` | High-dimensional document vector representation |
| **Orchestration** | LangChain Tool-Calling Agent | Dynamic routing between tools or direct LLM responses |
| **Vector Store** | ChromaDB (`langchain-chroma`) | Persisted local vector DB (337 chunks from 30 core docs) |
| **Backend API** | FastAPI + Uvicorn | Async REST API running on `http://127.0.0.1:8000` |
| **Observability** | SQLite (`logs.db`) | Automatic execution telemetry and latency tracking |
| **Frontend UI** | Streamlit (`app.py`) | Interactive full-stack web chat with status sidebars |

---

## 📊 Benchmark & Evaluation Results

Evaluated using an automated test harness (`eval.py`) across a structured 20-query evaluation dataset (`eval_dataset.json`):

| Metric | Result | Target / Standard |
| :--- | :--- | :--- |
| **Tool Routing Accuracy** | **100.0% (20/20)** | > 90% |
| **Tool Hallucination Rate** | **0.0%** | 0% |
| **Average Response Latency** | **6.22 seconds** | < 10.0s |

---

## 🚀 How to Run Locally

1. Create a `.env` file with `GOOGLE_API_KEY=your_key` and run `pip install -r requirements.txt`.
2. Launch the services:
   - Backend: `uvicorn main:app --reload`
   - Frontend: `streamlit run app.py`

---

## 📂 Repository Structure

```text
Rag-Agent/
├── app.py              # Streamlit chat web app (Frontend UI)
├── main.py             # FastAPI backend API server with SQLite logging
├── agent.py            # LangChain agent configuration & prompt logic
├── tools.py            # Custom tool belt (search_fastapi_docs & check_ticket_status)
├── ingest.py           # Document chunking & ChromaDB embedding pipeline
├── eval.py             # Automated benchmark evaluation harness
├── eval_dataset.json   # 20-case evaluation test dataset
└── eval_results.md     # Benchmarking results summary

```

```

---

### 🚀 Save 

1. Copy the block above and paste it into your local `README.md` file in VS Code.
2. Save the file (`Ctrl + S`).
3. Run these commands in your terminal to finalize your repository:

