from sqlalchemy.orm import sessionmaker

from ai_bi_assistant.database.connection import engine

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)