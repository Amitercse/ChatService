from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import Chroma
from services.gemini_model_configure import get_gemini_model, get_gemini_embeddings

DB_PATH = "vector_db/"

def get_conversational_chain():
    """
    Creates and returns a question-answering chain to process provided documents.
    """
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "I am sorry answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{input}\n

    Answer:
    """

    model = get_gemini_model()
    if not model:
        return None

    prompt = ChatPromptTemplate.from_template(prompt_template)
    return create_stuff_documents_chain(llm=model, prompt=prompt)

async def user_input(user_question: str):
    """
    Handles user input by querying the vector store and generating a response.
    """
    try:
        # Await the asynchronous function call
        embeddings = await get_gemini_embeddings()
        if not embeddings:
            return "Failed to initialize embeddings."

        vector_store = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
        docs = vector_store.similarity_search(user_question)

        if not docs:
            print("No relevant documents found. The knowledge base might be empty or the query is out of scope.")
            return "Answer is not available in the context."

        document_chain = get_conversational_chain()
        if not document_chain:
            return "Failed to create conversational chain."

        response = await document_chain.ainvoke(
            {
                "input": user_question,
                "context": docs
            }
        )
        return {"response": response}

    except Exception as e:
        print(f"An error occurred during user input processing: {e}")
        return "An error occurred while processing your request."