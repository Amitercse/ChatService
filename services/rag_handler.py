from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_community.vectorstores import Chroma
from services.gemini_model_configure import get_gemini_model, get_gemini_embeddings

DB_PATH = "vector_db/"

# The conversational chain is no longer the main logic, it becomes a "tool"
# This function is now a helper to create the retrieval tool.
def get_retrieval_tool(vector_store):
    from langchain.tools.retriever import create_retriever_tool
    retriever = vector_store.as_retriever()
    return create_retriever_tool(
        retriever,
        "knowledge_base_search",
        "Searches and returns information about Indian income tax rules, calculations, and concepts from the provided knowledge base. Use this tool for all tax-related questions."
    )

async def user_input(user_question: str):
    """
    Handles user input by initializing and running an agent to get a response.
    """
    try:
        # Await the asynchronous function call
        embeddings = await get_gemini_embeddings()
        if not embeddings:
            return "Failed to initialize embeddings."

        vector_store = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)

        # define tools
        tools = [get_retrieval_tool(vector_store)]

        # get llm models
        llm = get_gemini_model()
        if not llm:
            return "Failed to initialize the Gemini model."

        # Create prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant specialized in Indian income tax. Use the provided tools to answer user questions. If a question is not related to income tax and cannot be answered by your tools, state that you can only assist with tax-related queries."),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])

        # Create the agent with tool calling capabilities
        agent = create_tool_calling_agent(llm, tools, prompt)

        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        response = await agent_executor.ainvoke({"input": user_question, "chat_history": []})
        return {"response": response['output']}

    except Exception as e:
        print(f"An error occurred during user input processing: {e}")
        return "An error occurred while processing your request."