from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

_embeddings = None
_vector_db = None


def get_vector_db():
    """
    Load the embedding model and Chroma database only once.
    """

    global _embeddings
    global _vector_db

    if _vector_db is None:

        print("Loading embedding model...")

        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        print("Loading Chroma database...")

        _vector_db = Chroma(
            persist_directory="chroma_db",
            embedding_function=_embeddings,
        )

        print("Vector database ready.")

    return _vector_db


def retrieve_documents(question: str, k: int = 2):
    """
    Retrieve relevant document chunks.
    """

    vector_db = get_vector_db()

    return vector_db.similarity_search(
        question,
        k=k,
    )