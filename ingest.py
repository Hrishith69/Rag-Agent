import os
import time
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

def build_vector_database():
    docs_path = Path("fastapi/docs/en/docs")
    if not docs_path.exists():
        print("❌ Error: Could not find documentation folder.")
        return

    # 1. Gather the first 30 files alphabetically
    all_files = sorted(list(docs_path.glob("**/*.md")))
    target_files = all_files[:30]
    
    raw_texts = []
    metadatas = []
    
    print(f"📚 Reading {len(target_files)} sample files...")
    for file in target_files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                raw_texts.append(f.read())
                # Attach the relative file path so query.py can cite it later
                metadatas.append({"source": str(file.relative_to(docs_path))})
        except Exception:
            continue

    # 2. Chunk text while preserving metadata association
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=60)
    chunks = text_splitter.create_documents(raw_texts, metadatas=metadatas)
    print(f"🧩 Chopped docs into {len(chunks)} chunks with exact file tracking.")

    # 3. Initialize embedding model
    print("🧠 Generating embeddings via Google AI Studio...")
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

    # 4. Save to Chroma in safe, paced sub-batches
    db_storage_path = "./chroma_db"
    batch_size = 25  # Reduced from 50 to prevent hitting the 100 RPM ceiling
    print(f"💾 Saving chunks to local Chroma database in batches of {batch_size}...")
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        Chroma.from_documents(
            documents=batch,
            embedding=embeddings,
            persist_directory=db_storage_path
        )
        processed_count = min(i + batch_size, len(chunks))
        print(f"✅ Processed {processed_count}/{len(chunks)} chunks...")
        
        if processed_count < len(chunks):
            print("⏳ Pausing 20 seconds to safely stay under Google's rate limits...")
            time.sleep(20)

    print(f"🎉 Success! Clean vector database created at: {db_storage_path}")

if __name__ == "__main__":
    build_vector_database()