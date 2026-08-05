def route_question(question: str) -> str:
    """
    Routes the question to:
    - sql
    - rag
    - hybrid
    """

    q = question.lower()

    hybrid_keywords = [
        "compare",
        "comparison",
        "versus",
        "vs",
        "against",
        "along with",
        "our",
    ]

    rag_keywords = [
        "spotify",
        "annual report",
        "report",
        "strategy",
        "risk",
        "financial risk",
        "ceo",
        "business model",
        "mission",
        "vision",
        "future",
        "investor",
        "shareholder",
        "20-f",
        "filing",
        "management",
        "chairman",
        "ai",
        "machine learning",
    ]

    sql_keywords = [
        "revenue",
        "sales",
        "artist",
        "genre",
        "country",
        "stream",
        "streams",
        "monthly",
        "yearly",
        "growth",
        "profit",
        "customers",
        "users",
    ]

    has_sql = any(word in q for word in sql_keywords)
    has_rag = any(word in q for word in rag_keywords)
    has_compare = any(word in q for word in hybrid_keywords)

    if has_compare and has_sql and has_rag:
        return "hybrid"

    if has_rag and not has_sql:
        return "rag"

    return "sql"