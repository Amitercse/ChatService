import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import Chroma
from services.gemini_model_configure import get_gemini_embeddings
import asyncio

# path of knowledge base and vector db are in parent folder of current file that is main parent folder of our app
DATA_PATH = "../knowledge_base"
DB_PATH = "../vector_db/"

def create_vector_db():
    """
    Creates a vector database from PDF documents.
    """

    if not os.path.exists(DATA_PATH):
        print(f"Data directory '{DATA_PATH}' not found.")
        return

    try:
        loader = PyPDFDirectoryLoader(DATA_PATH)
        documents = loader.load()
        print(f"Number of documents loaded: {len(documents)}")
        if not documents:
            print("No documents loaded. Check your data directory and PDF files.")
            return

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)
        print(f"Number of text chunks created: {len(texts)}")
        if not texts:
            print("Failed to split documents into texts.")
            return

        # Use asyncio.run to execute the async function
        embeddings = asyncio.run(get_gemini_embeddings())
        if not embeddings:
            print("Failed to initialize embeddings model.")
            return

        if os.path.exists(DB_PATH):
            import shutil
            shutil.rmtree(DB_PATH)

        Chroma.from_documents(texts, embeddings, persist_directory=DB_PATH)
        print("Vector database created successfully.")

    except Exception as e:
        print(f"An error occurred during vector database creation: {e}")

"""
Execute this file separately and not with main app to create embeddings before app executes.
That's why exposed main function here, can also expose rest API to invoke create_vector_db() and update embeddings at runtime
"""
if __name__ == '__main__':
    create_vector_db()