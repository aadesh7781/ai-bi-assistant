import os

from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()

_embeddings = None
_vector_db = None


def get_vector_db():
    global _embeddings
    global _vector_db

    if _vector_db is None:

        print("Loading Jina embeddings...")

        _embeddings = OpenAIEmbeddings(
            api_key=os.getenv("JINA_API_KEY"),
            base_url="https://api.jina.ai/v1",
            model="jina-embeddings-v3",
        )

        print("Opening Chroma...")

        _vector_db = Chroma(
            persist_directory="chroma_db",
            embedding_function=_embeddings,
        )

        print("Vector DB ready.")

    return _vector_db


def retrieve_documents(question: str, k: int = 2):

    vector_db = get_vector_db()

    return vector_db.similarity_search(
        question,
        k=k,
    )