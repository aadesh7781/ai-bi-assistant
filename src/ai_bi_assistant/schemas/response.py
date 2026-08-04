from pydantic import BaseModel


class ChatResponse(BaseModel):
    question: str
    answer: str
    generated_sql: str
    rows: list