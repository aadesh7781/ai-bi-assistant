from langchain_core.prompts import ChatPromptTemplate

from ai_bi_assistant.agents.llm import llm

prompt = ChatPromptTemplate.from_template(
"""
You are a senior Business Intelligence Analyst.

A SQL query has already been executed.

Question:
{question}

SQL Result:
{rows}

Write a concise business-friendly answer.

Rules:
- Do not mention SQL.
- Mention important numbers.
- Be concise (3-6 sentences).
- If the result is empty, explain that no matching data was found.
"""
)

chain = prompt | llm


def generate_response(question: str, rows):
    response = chain.invoke(
        {
            "question": question,
            "rows": rows,
        }
    )

    return response.content