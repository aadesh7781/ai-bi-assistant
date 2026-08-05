import json

from langchain_core.prompts import ChatPromptTemplate

from ai_bi_assistant.agents.llm import llm


prompt = ChatPromptTemplate.from_template(
"""
You are an AI planner.

Split the user's question into two parts.

Return ONLY valid JSON with exactly these keys:

- sql_question
- rag_question

Rules:

- sql_question should contain ONLY the database-related part.
- rag_question should contain ONLY the document/report-related part.
- If one part is unnecessary, return an empty string.
- Return ONLY JSON.
- Do not wrap the JSON in markdown.

User Question:

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

    return json.loads(text)