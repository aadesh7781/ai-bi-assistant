from ai_bi_assistant.database.connection import engine
from ai_bi_assistant.models.base import Base

# Import all models
from ai_bi_assistant.models.label import Label
from ai_bi_assistant.models.genre import Genre
from ai_bi_assistant.models.country import Country


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")


if __name__ == "__main__":
    create_tables()