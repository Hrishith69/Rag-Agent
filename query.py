import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def run_retrieval_pipeline():
    # 1. Verify Authentication
    if "GEMINI_API_KEY" not in os.environ:
        print("❌ Error: GEMINI_API_KEY environment variable is not set!")
        return

    print("🔍 Connecting to local Chroma database...")
    db_storage_path = "./chroma_db"
    
    # 2. Re-initialize Embedding Model
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    
    # 3. Load Vector Database from Disk
    db = Chroma(persist_directory=db_storage_path, embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 3})
    
    # 4. Accept User Question
    question = input("\n📥 Enter your technical question about FastAPI: ")
    if not question.strip():
        print("⚠️ Question cannot be empty. Exiting.")
        return
        
    print("🧠 Searching matching documentation chunks...")
    docs = retriever.invoke(question)
    
    if not docs:
        print("❌ No relevant documentation chunks found matching your query.")
        return
        
    # 5. Format Context Blocks with Metadata Sources
    context_chunks = []
    for doc in docs:
        source_file = doc.metadata.get('source', 'Unknown File')
        context_chunks.append(f"--- Source: {source_file} ---\n{doc.page_content}")
    
    context_text = "\n\n".join(context_chunks)
    
    # 6. Initialize LLM & Prompt Template
    llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0)
    
    prompt_template = ChatPromptTemplate.from_template(
        "You are a production-grade Technical Support AI Assistant for FastAPI.\n"
        "Answer the question accurately using ONLY the provided context blocks below. "
        "If the answer cannot be found in the context, explicitly say 'I don't know based on the current documentation.'\n"
        "For every code pattern or major statement you make, cite the corresponding Source filename.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answer:"
    )
    
    # 7. Execute Chain
    chain = prompt_template | llm | StrOutputParser()
    response = chain.invoke({"context": context_text, "question": question})
    
    # 8. Output Results
    print("\n🤖 AI Answer:")
    print(response)
    print("\n📚 Raw Sources Extracted:")
    for idx, doc in enumerate(docs, 1):
        print(f"  [{idx}] {doc.metadata.get('source', 'Unknown')}")

if __name__ == "__main__":
    run_retrieval_pipeline()