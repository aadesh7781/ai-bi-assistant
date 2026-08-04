from sqlalchemy import text

from ai_bi_assistant.database.connection import engine


def run_query(query: str):
    """
    Execute a SQL query and return all rows.
    """

    with engine.connect() as conn:
        result = conn.execute(text(query))

        return result.mappings().all()