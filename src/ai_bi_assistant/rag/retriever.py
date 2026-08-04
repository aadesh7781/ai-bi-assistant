from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

print("Starting retriever module...")

print("Creating embeddings...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
print("Embeddings created.")

print("Opening Chroma...")
vector_db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings,
)
print("Chroma opened.")

def retrieve_documents(question: str, k: int = 2):
    print("Searching...")
    return vector_db.similarity_search(question, k=k)