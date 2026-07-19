import os
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

def smoke_test_ingestion():
    docs_path = Path("fastapi/docs/en/docs")
    if not docs_path.exists():
        return

    # Take EXACTLY 1 file to guarantee we don't trigger the daily limit
    md_files = list(docs_path.glob("**/*.md"))[:30]
    
    raw_texts = []
    with open(md_files[0], "r", encoding="utf-8") as f:
        raw_texts.append(f.read())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=60)
    chunks = text_splitter.create_documents(raw_texts)
    print(f"🧩 Chopped 30 test file into {len(chunks)} chunks.")

    print(f"🧠 Testing embeddings with a fresh project key...")
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    
    db_storage_path = "./chroma_db"
    Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=db_storage_path)
    print(f"🎉 Success! Vector database created locally at: {db_storage_path}")

if __name__ == "__main__":
    smoke_test_ingestion()