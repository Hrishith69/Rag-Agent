import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from tools import search_fastapi_docs, check_ticket_status

def build_triage_agent():
    # 1. Initialize Gemini LLM (temperature=0 for factual accuracy)
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        temperature=0
    )

    # 2. Bundle our tools together
    tools = [search_fastapi_docs, check_ticket_status]

    # 3. Create the System Prompt instructing the agent on how to behave
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are an expert Technical Support and Document Triage Agent for FastAPI.\n"
         "You have access to tools to search technical documentation and check support ticket status.\n"
         "Rules:\n"
         "1. If asked a technical question about FastAPI, use the 'search_fastapi_docs' tool.\n"
         "2. If asked about a ticket status or ID (e.g., TCK-101), use the 'check_ticket_status' tool.\n"
         "3. For general conversation or greetings, answer directly without calling tools.\n"
         "4. If documentation does not contain the answer, state clearly that you don't know based on available docs."
        ),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])

    # 4. Construct the Tool-Calling Agent & Executor Loop
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor

if __name__ == "__main__":
    agent_chain = build_triage_agent()
    
    print("🤖 Agent Online! Ask a technical question, check a ticket (e.g., TCK-101), or say hello.\n")
    user_query = input("💬 User Input: ")
    
    response = agent_chain.invoke({"input": user_query})
    print("\n🤖 Final Agent Response:")
    
    # Clean output extraction for Gemini response blocks
    output = response["output"]
    if isinstance(output, list) and len(output) > 0 and isinstance(output[0], dict) and "text" in output[0]:
        print(output[0]["text"])
    else:
        print(output)