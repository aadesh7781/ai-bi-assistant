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

=========================================================
SQL RESULTS
=========================================================

{sql_results}

=========================================================
DOCUMENT CONTEXT
=========================================================

{document_context}

=========================================================
USER QUESTION
=========================================================

{question}

Instructions:

1. Use BOTH SQL results and document context whenever available.

2. Treat SQL results as factual.
   - Never modify SQL values.
   - Never estimate SQL values.
   - Never perform your own calculations.

3. Treat document context as factual.
   - Carefully inspect paragraphs AND tables.
   - If financial tables contain revenue, growth,
     subscribers, MAUs, operating income or other
     numeric values, extract those values exactly.
   - Never say information is unavailable if it
     exists anywhere in the retrieved context.

4. For comparison questions:
   - Compare SQL values with annual report values.
   - Mention differences in units or currencies.
   - Explain clearly if comparison cannot be made.

5. If only SQL exists:
   Answer using SQL only.

6. If only document context exists:
   Answer using the annual report only.

7. Structure your answer like this:

Executive Summary

SQL Insights
- ...

Annual Report Insights
- ...

Comparison
- ...

8. Whenever you use document information,
mention the source file and page number.

Example:

Source:
Annual-Report-2024.pdf
Page 151

9. If multiple documents support the answer,
cite each source separately.

10. Never invent numbers.

11. Never invent citations.

12. Never use external knowledge.

Return ONLY the final answer.
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

            validate_sql(sql)

            rows = execute_sql(sql)

            print(f"Rows Returned: {len(rows)}")

        sql_summary = summarize_sql(rows)

        # --------------------------------------------
        # Step 3 : RAG
        # --------------------------------------------

        document_context = ""

        if rag_question:

            print("Retrieving documents...")

            docs = retrieve_documents(
                rag_question,
                k=8,
            )

            print(f"Retrieved {len(docs)} documents.")

            context_parts = []

            for i, doc in enumerate(docs, start=1):

                source = doc.metadata.get(
                    "source",
                    "Unknown"
                )

                source = source.split("/")[-1].split("\\")[-1]

                page = doc.metadata.get(
                    "page",
                    "Unknown"
                )

                context_parts.append(
f"""
==================================================
DOCUMENT {i}

SOURCE FILE:
{source}

PAGE:
{page}

CONTENT:

{doc.page_content}

==================================================
"""
                )

            document_context = "\n".join(context_parts)

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