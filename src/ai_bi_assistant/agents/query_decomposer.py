import json

from langchain_core.prompts import ChatPromptTemplate

from ai_bi_assistant.agents.llm import llm


prompt = ChatPromptTemplate.from_template(
"""
You are an AI Business Intelligence planner.

Your ONLY job is to split the user's question into two natural language questions.

DO NOT generate SQL.
DO NOT generate database queries.
DO NOT write SELECT statements.

Return ONLY valid JSON in this format:

{{
    "sql_question": "...",
    "rag_question": "..."
}}

Rules:

1. sql_question should describe ONLY the information needed from the SQL database.
2. rag_question should describe ONLY the information needed from the uploaded reports.
3. Both questions MUST remain in plain English.
4. If SQL is not required, return "".
5. If RAG is not required, return "".
6. Never invent information.
7. Never output markdown.

Examples

User:
Show revenue by country.

Output:
{{
    "sql_question": "Show revenue by country.",
    "rag_question": ""
}}

User:
What is Spotify's AI strategy?

Output:
{{
    "sql_question": "",
    "rag_question": "What is Spotify's AI strategy according to the annual report?"
}}

User:
Compare our revenue with Spotify's reported revenue.

Output:
{{
    "sql_question": "What is our total revenue?",
    "rag_question": "What revenue did Spotify report in its annual report?"
}}

User:
Compare our growth with Spotify's reported growth.

Output:
{{
    "sql_question": "What is our revenue growth?",
    "rag_question": "What growth did Spotify report in its annual report?"
}}

Question:

{question}
"""
)

chain = prompt | llm


def decompose_question(question: str):

    response = chain.invoke(
        {
            "question": question
        }
    )

    text = response.content.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "", 1)

    if text.startswith("```"):
        text = text.replace("```", "", 1)

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    print("=" * 70)
    print("DECOMPOSER OUTPUT")
    print(text)
    print("=" * 70)

    return json.loads(text)