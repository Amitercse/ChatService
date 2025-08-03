from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

# It is recommended to use environment variables for your API key
# Example: export GEMINI_API_KEY="your_key_here"
GEMINI_API_KEY = ""

if not GEMINI_API_KEY:
    print("GEMINI_API_KEY is not set.")

def get_gemini_model():
    """Initializes and returns the Gemini chat model as a LangChain Runnable."""
    try:
        # Use ChatGoogleGenerativeAI, which is a LangChain Runnable
        model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=GEMINI_API_KEY,
            model_kwargs={"generation_config": {"response_mime_type": "application/json"}}
        )
        return model
    except Exception as e:
        print(f"Error configuring Gemini API: {e}")
        return None

async def get_gemini_embeddings():
    """Initializes and returns the Gemini embedding model asynchronously."""
    try:
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=GEMINI_API_KEY
        )
        return embeddings
    except Exception as e:
        print(f"Error configuring Gemini API for embeddings: {e}")
        return None