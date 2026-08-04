from fastapi import FastAPI

from ai_bi_assistant.schemas.response import ChatResponse
from ai_bi_assistant.schemas.chat import ChatRequest

from ai_bi_assistant.agents.sql_generator import generate_sql
from ai_bi_assistant.agents.validator import validate_sql
from ai_bi_assistant.agents.sql_executor import execute_sql
from ai_bi_assistant.agents.response_generator import generate_response

from ai_bi_assistant.agents.router import route_question
from ai_bi_assistant.agents.hybrid import hybrid_answer
from ai_bi_assistant.rag.qa import answer_question


app = FastAPI(
    title="AI Business Intelligence Assistant",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "AI BI Assistant API is running!"
    }


@app.post("/ask", response_model=ChatResponse)
def ask(request: ChatRequest):

    # ==========================================
    # Decide which pipeline should answer
    # ==========================================

    mode = route_question(request.question)

    print(f"Pipeline Selected: {mode}")

    # ==========================================
    # RAG
    # ==========================================

    if mode == "rag":

        answer = answer_question(request.question)

        return {
            "question": request.question,
            "answer": answer,
            "generated_sql": "",
            "rows": [],
        }

    # ==========================================
    # HYBRID
    # ==========================================

    if mode == "hybrid":

        result = hybrid_answer(request.question)

        return {
            "question": request.question,
            "answer": result["answer"],
            "generated_sql": result["sql"],
            "rows": result["rows"],
        }

    # ==========================================
    # SQL
    # ==========================================

    sql = generate_sql(request.question)

    validate_sql(sql)

    rows = execute_sql(sql)

    answer = generate_response(
        request.question,
        rows,
    )

    return {
        "question": request.question,
        "answer": answer,
        "generated_sql": sql,
        "rows": rows,
    }