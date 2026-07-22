import streamlit as st
import requests
import time

# ---------------------------------------------------------
# Page Config & Title
# ---------------------------------------------------------
st.set_page_config(
    page_title="Support Ticket & Doc Triage Agent", 
    page_icon="🤖", 
    layout="wide"
)

# ---------------------------------------------------------
# Sidebar: System Status & Demo Guide
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ System Status")
    st.success("🟢 FastAPI Backend: Connected")
    st.info("🧠 Model: gemini-3.1-flash-lite")
    st.info("📚 Vector Store: ChromaDB (337 chunks)")
    st.info("🗄️ Logging: SQLite (logs.db)")
    
    st.divider()
    
    st.header("💡 What to Ask")
    st.markdown("""
    **1. Doc Retrieval (RAG):**
    - *How do I define path parameters in FastAPI?*
    - *What are query parameters?*
    
    **2. Ticket Lookup Tool:**
    - *Check status for ticket TCK-101*
    - *What is the state of TCK-102?*
    
    **3. Casual Chat:**
    - *Hello! Who are you?*
    
    **4. Out of Scope:**
    - *Who won the 1998 World Cup?*
    """)

# ---------------------------------------------------------
# Main Page Header
# ---------------------------------------------------------
st.title("🤖 Support Ticket & Technical Doc Triage Agent")
st.caption("Flagship Portfolio RAG System — LangChain, ChromaDB, Gemini & FastAPI")

FASTAPI_URL = "http://127.0.0.1:8000/chat"

# Initialize Session Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Chat Input
if user_query := st.chat_input("Type your technical question or ticket ID (e.g., TCK-101)..."):
    # Store and show User Message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Process Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("🤖 Agent analyzing query and selecting tools..."):
            try:
                start_time = time.time()
                response = requests.post(
                    FASTAPI_URL, 
                    json={"prompt": user_query}, 
                    timeout=60
                )
                elapsed_time = round(time.time() - start_time, 2)

                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("response", "No response content received.")
                    
                    # Output Answer & Performance Badge
                    st.markdown(answer)
                    st.caption(f"⚡ Latency: {elapsed_time}s | Status: 200 OK")
                    
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"❌ Error {response.status_code}: Unable to process query.")
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection Failed! Ensure `uvicorn main:app --reload` is running in Terminal 1.")