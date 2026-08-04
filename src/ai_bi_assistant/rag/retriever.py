from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings,
)


def retrieve_documents(question: str, k: int = 4):
    """
    Retrieve the most relevant document chunks.
    """

    docs = vector_db.similarity_search(
        question,
        k=k,
    )

    return docs