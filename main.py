import sqlite3
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import build_triage_agent

app = FastAPI(
    title="Support Ticket & Document Triage Agent API",
    description="Backend API powered by Gemini & LangChain with SQLite interaction logging."
)

# Initialize SQLite database for logging
def init_db():
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            prompt TEXT,
            response TEXT,
            latency_seconds REAL
        )
    """)
    conn.commit()
    conn.close()

# Run database setup on startup
init_db()

# Build Agent Executor instance
agent_executor = build_triage_agent()

class QueryRequest(BaseModel):
    prompt: str

class QueryResponse(BaseModel):
    prompt: str
    response: str
    latency_seconds: float

@app.get("/")
def health_check():
    return {"status": "online", "message": "Support Triage Agent API is running."}

@app.post("/chat", response_model=QueryResponse)
def chat_endpoint(request: QueryRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")
    
    start_time = time.time()
    
    try:
        result = agent_executor.invoke({"input": request.prompt})
        output = result["output"]
        
        # Clean response extraction
        if isinstance(output, list) and len(output) > 0 and isinstance(output[0], dict) and "text" in output[0]:
            clean_text = output[0]["text"]
        else:
            clean_text = str(output)
            
        latency = round(time.time() - start_time, 2)
        
        # Log interaction to SQLite
        conn = sqlite3.connect("logs.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_logs (prompt, response, latency_seconds) VALUES (?, ?, ?)",
            (request.prompt, clean_text, latency)
        )
        conn.commit()
        conn.close()
        
        return QueryResponse(prompt=request.prompt, response=clean_text, latency_seconds=latency)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")