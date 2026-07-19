import os
from langchain_google_genai import ChatGoogleGenerativeAI

def test_api_connection():
    if "GEMINI_API_KEY" not in os.environ:
        print("❌ Error: GEMINI_API_KEY environment variable is not set!")
        return

    print("🤖 Connecting to Gemini via LangChain...")
    try:
        # We updated this parameter to match your active model list
        llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0.2)
        response = llm.invoke("System check. Reply with exactly three words: 'System online, captain.'")
        print(f"\n🎉 Success!\n👉 {response.content}")
    except Exception as e:
        print(f"\n❌ Connection failed:\n{e}")

if __name__ == "__main__":
    test_api_connection()