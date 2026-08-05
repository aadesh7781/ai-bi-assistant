import traceback
import pandas as pd

from langchain_core.prompts import ChatPromptTemplate

from ai_bi_assistant.agents.llm import llm
from ai_bi_assistant.agents.query_decomposer import decompose_question

from ai_bi_assistant.agents.sql_generator import generate_sql
from ai_bi_assistant.agents.sql_executor import execute_sql
from ai_bi_assistant.agents.validator import validate_sql

from ai_bi_assistant.rag.retriever import retrieve_documents


# =====================================================
# Prompt
# =====================================================

prompt = ChatPromptTemplate.from_template(
"""
You are a Senior Business Intelligence Analyst.

You have two independent sources of information.

====================================================
SQL RESULTS
====================================================

{sql_results}

====================================================
DOCUMENT CONTEXT
====================================================

{document_context}

====================================================
QUESTION
====================================================

{question}

Instructions:

- Use BOTH SQL results and document context.
- Never invent numbers.
- Never estimate missing values.
- Never perform arithmetic or calculations.
- Use SQL values exactly as provided.
- If comparison is impossible, clearly explain why.
- Mention which insights came from SQL and which came from the annual report.
- Give a concise executive summary.
- Do NOT explain your reasoning.
- Return only the final answer.
"""
)

chain = prompt | llm


# =====================================================
# SQL Summarizer
# =====================================================

def summarize_sql(rows):

    if not rows:
        return "No SQL results were returned."

    df = pd.DataFrame(rows)

    summary = []

    summary.append(f"Rows Returned: {len(df)}")
    summary.append(f"Columns: {', '.join(df.columns)}")
    summary.append("")
    summary.append(df.head(10).to_string(index=False))

    return "\n".join(summary)


# =====================================================
# Hybrid Pipeline
# =====================================================

def hybrid_answer(question: str):

    try:

        # --------------------------------------------
        # Step 1 : Decompose Question
        # --------------------------------------------

        parts = decompose_question(question)

        print("=" * 80)
        print("DECOMPOSER OUTPUT")
        print(parts)
        print("=" * 80)

        sql_question = parts.get("sql_question", "").strip()
        rag_question = parts.get("rag_question", "").strip()

        print("=" * 80)
        print("SQL QUESTION")
        print(repr(sql_question))

        print("=" * 80)
        print("RAG QUESTION")
        print(repr(rag_question))
        print("=" * 80)

        # --------------------------------------------
        # Step 2 : SQL
        # --------------------------------------------

        rows = []
        sql = ""

        if sql_question:

            print("Generating SQL...")

            sql = generate_sql(sql_question)

            print("=" * 80)
            print("GENERATED SQL")
            print(sql)
            print("=" * 80)

            print("Validating SQL...")
            validate_sql(sql)
            print("SQL VALIDATED")

            print("Executing SQL...")

            rows = execute_sql(sql)

            print(f"ROWS RETURNED: {len(rows)}")

        sql_summary = summarize_sql(rows)

        # --------------------------------------------
        # Step 3 : Retrieve Documents
        # --------------------------------------------

        document_context = ""

        if rag_question:

            print("Retrieving RAG documents...")

            docs = retrieve_documents(
                rag_question,
                k=5,
            )

            print(f"Retrieved {len(docs)} documents.")

            document_context = "\n\n".join(
                doc.page_content
                for doc in docs
            )

        # --------------------------------------------
        # Step 4 : Final LLM
        # --------------------------------------------

        print("Generating final answer...")

        response = chain.invoke(
            {
                "question": question,
                "sql_results": sql_summary,
                "document_context": document_context,
            }
        )

        print("Hybrid pipeline completed successfully.")

        return {
            "answer": response.content,
            "sql": sql,
            "rows": rows,
        }

    except Exception:

        print("=" * 80)
        print("HYBRID PIPELINE ERROR")
        traceback.print_exc()
        print("=" * 80)

        raise