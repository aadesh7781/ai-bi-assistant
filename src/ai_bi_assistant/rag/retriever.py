import os
import requests

from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_core.embeddings import Embeddings

load_dotenv()


# =====================================================
# Jina Embeddings
# =====================================================

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

        response.raise_for_status()

        return response.json()["data"][0]["embedding"]


# =====================================================
# Singleton Chroma
# =====================================================

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


# =====================================================
# Query Expansion
# =====================================================

def expand_query(question: str):

    q = question.lower()

    expanded = {question}

    # -----------------------------------------
    # CEO LETTER
    # -----------------------------------------

    if "ceo" in q or "shareholder" in q or "letter" in q:

        expanded.update([
            "Letter to Shareholders",
            "Shareholder Letter",
            "Letter from Daniel Ek",
            "Daniel Ek",
            "Founder Letter",
            "Message from CEO",
        ])

    # -----------------------------------------
    # BUSINESS MODEL
    # -----------------------------------------

    if "business model" in q or "how spotify makes money" in q:

        expanded.update([
            "Business Model",
            "Premium",
            "Ad-Supported",
            "Subscriptions",
            "Marketplace",
            "Monetization",
        ])

    # -----------------------------------------
    # REVENUE
    # -----------------------------------------

    if "revenue" in q:

        expanded.update([
            "Consolidated Revenue",
            "Financial Statements",
            "Income Statement",
            "Financial Highlights",
            "Net Revenue",
            "Revenue Growth",
        ])

    # -----------------------------------------
    # GROWTH
    # -----------------------------------------

    if "growth" in q:

        expanded.update([
            "Year-over-year",
            "YoY",
            "Premium Subscribers",
            "Monthly Active Users",
            "MAUs",
            "Financial Highlights",
        ])

    # -----------------------------------------
    # AI
    # -----------------------------------------

    if "ai" in q or "artificial intelligence" in q:

        expanded.update([
            "Machine Learning",
            "Artificial Intelligence",
            "Algorithms",
            "Recommendation System",
            "AI Playlist",
            "AI DJ",
            "AI investments",
            "Personalization",
        ])

    # -----------------------------------------
    # Podcasts
    # -----------------------------------------

    if "podcast" in q:

        expanded.update([
            "Podcast",
            "Podcasts",
            "Podcast Business",
            "Podcast Strategy",
            "Creators",
        ])

    # -----------------------------------------
    # Audiobooks
    # -----------------------------------------

    if "audiobook" in q:

        expanded.update([
            "Audiobooks",
            "Audiobook Strategy",
        ])

    # -----------------------------------------
    # Risks
    # -----------------------------------------

    if "risk" in q:

        expanded.update([
            "Risk Factors",
            "Financial Risks",
            "Business Risks",
            "Operational Risks",
        ])

    return list(expanded)


# =====================================================
# Retriever
# =====================================================

def retrieve_documents(question: str, k: int = 8):

    print("=" * 80)
    print("QUESTION:", question)
    print("=" * 80)

    vector_db = get_vector_db()

    queries = expand_query(question)

    print("\nExpanded Queries:")

    for q in queries:
        print("-", q)

    print()

    documents = []
    seen = set()

    for q in queries:

        docs = vector_db.max_marginal_relevance_search(
            query=q,
            k=3,
            fetch_k=20,
        )

        for doc in docs:

            key = (
                doc.metadata.get("source"),
                doc.metadata.get("page"),
            )

            if key not in seen:
                seen.add(key)
                documents.append(doc)

    print(f"Retrieved {len(documents)} unique documents.")

    return documents[:k]