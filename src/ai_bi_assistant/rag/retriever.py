import os
import requests

from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_core.embeddings import Embeddings

load_dotenv()


class JinaEmbeddings(Embeddings):
    def __init__(self):
        self.api_key = os.getenv("JINA_API_KEY")
        self.url = "https://api.jina.ai/v1/embeddings"
        self.model = "jina-embeddings-v3"

    def embed_documents(self, texts):
        embeddings = []

        for text in texts:
            response = requests.post(
                self.url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "input": text,
                },
                timeout=60,
            )

            response.raise_for_status()

            embeddings.append(
                response.json()["data"][0]["embedding"]
            )

        return embeddings

    def embed_query(self, text):

        print("=" * 80)
        print("EMBED QUERY CALLED")
        print("VALUE :", repr(text))
        print("TYPE  :", type(text))
        print("=" * 80)

        response = requests.post(
            self.url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "input": str(text),
            },
            timeout=60,
        )

        print("STATUS:", response.status_code)
        print("BODY:", response.text)

        response.raise_for_status()

        return response.json()["data"][0]["embedding"]


_embeddings = None
_vector_db = None


def get_vector_db():
    global _embeddings
    global _vector_db

    if _vector_db is None:

        print("Loading Jina embeddings...")

        _embeddings = JinaEmbeddings()

        print("Opening Chroma database...")

        _vector_db = Chroma(
            persist_directory="chroma_db",
            embedding_function=_embeddings,
        )

        print("Vector database ready.")

    return _vector_db


def retrieve_documents(question: str, k: int = 2):

    print("=" * 60)
    print("QUESTION:", repr(question))
    print("TYPE:", type(question))
    print("=" * 60)

    vector_db = get_vector_db()

    docs = vector_db.similarity_search(
        str(question),
        k=k,
    )

    print(f"Retrieved {len(docs)} documents.")

    return docs