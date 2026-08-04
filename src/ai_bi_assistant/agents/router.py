def route_question(question: str) -> str:
    """
    Route a user question to one of:
    - sql
    - rag
    - hybrid
    """

    q = question.lower()

    # ===========================
    # Hybrid Keywords
    # ===========================

    hybrid_keywords = [
        "compare",
        "comparison",
        "versus",
        "vs",
        "against",
        "along with",
        "according to",
        "how does our",
        "compare our",
        "our data and",
        "our revenue and",
        "our streams and",
        "our popularity and",
    ]

    # ===========================
    # RAG Keywords
    # ===========================

    rag_keywords = [
        "annual report",
        "report",
        "strategy",
        "risk",
        "spotify",
        "ceo",
        "podcast",
        "podcasts",
        "audiobook",
        "audiobooks",
        "investor",
        "shareholder",
        "business model",
        "mission",
        "vision",
        "future plans",
        "financial report",
        "20-f",
        "filing",
        "management",
        "chairman",
    ]

    # ----------------------------
    # HYBRID FIRST
    # ----------------------------

    if any(keyword in q for keyword in hybrid_keywords):

        if any(keyword in q for keyword in rag_keywords):
            return "hybrid"

        return "sql"

    # ----------------------------
    # RAG
    # ----------------------------

    if any(keyword in q for keyword in rag_keywords):
        return "rag"

    # ----------------------------
    # SQL
    # ----------------------------

    return "sql"