import json

from langchain_core.prompts import ChatPromptTemplate

from ai_bi_assistant.agents.llm import llm


prompt = ChatPromptTemplate.from_template("""
You are an AI planner.

Split the user's question into:

1. sql_question
2. rag_question

Rules:

- sql_question should contain ONLY the database part.
- rag_question should contain ONLY the document/report part.
- If one is unnecessary, return an empty string.
- NEVER return null.
- Return ONLY valid JSON.

Example output:

{
    "sql_question": "Show monthly revenue.",
    "rag_question": "What does Spotify's annual report say about revenue?"
}

Question:

{question}
""")

chain = prompt | llm


def decompose_question(question: str):

    response = chain.invoke(
        {
            "question": question
        }
    )

    text = response.content.strip()

    print("=" * 70)
    print("RAW LLM RESPONSE")
    print(text)
    print("=" * 70)

    if text.startswith("```json"):
        text = text.replace("```json", "", 1)

    if text.startswith("```"):
        text = text.replace("```", "", 1)

    if text.endswith("```"):
        text = text[:-3]

    result = json.loads(text)

    sql_question = result.get("sql_question") or ""
    rag_question = result.get("rag_question") or ""

    print("SQL QUESTION:", repr(sql_question))
    print("RAG QUESTION:", repr(rag_question))
    print("=" * 70)

    return {
        "sql_question": sql_question,
        "rag_question": rag_question,
    }