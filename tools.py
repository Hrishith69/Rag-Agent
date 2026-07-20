import os
from langchain_core.tools import tool
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

@tool
def search_fastapi_docs(query: str) -> str:
    """Searches the official FastAPI documentation vector database for technical questions, path parameters, dependency injection, and code examples."""
    db_storage_path = "./chroma_db"
    
    if not os.path.exists(db_storage_path):
        return "Error: Local vector store database standard directory missing."

    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    database = Chroma(
        persist_directory=db_storage_path,
        embedding_function=embeddings
    )
    
    # Retrieve top 3 relevant chunks
    matches = database.similarity_search(query, k=3)
    if not matches:
        return "No relevant documentation found for this query."
    
    results = []
    for doc in matches:
        source_file = doc.metadata.get("source", "Unknown File")
        results.append(f"[Source: {source_file}]\n{doc.page_content}")
        
    return "\n\n---\n\n".join(results)


@tool
def check_ticket_status(ticket_id: str) -> str:
    """Looks up the status, priority, and assigned details of a support ticket using its Ticket ID (e.g., TCK-101)."""
    # Mock database dictionary representing customer support ticket records
    mock_tickets = {
        "TCK-101": "Ticket ID: TCK-101 | Status: OPEN | Priority: HIGH | Issue: Database connection pooling failure in production.",
        "TCK-102": "Ticket ID: TCK-102 | Status: IN_PROGRESS | Priority: MEDIUM | Issue: How to configure CORS headers for Streamlit frontend.",
        "TCK-103": "Ticket ID: TCK-103 | Status: CLOSED | Priority: LOW | Issue: Syntax question regarding Pydantic model validation errors."
    }
    
    clean_id = ticket_id.strip().upper()
    return mock_tickets.get(clean_id, f"Ticket ID '{ticket_id}' was not found in the triage database.")