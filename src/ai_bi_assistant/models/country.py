from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ai_bi_assistant.models.base import Base


class Country(Base):
    __tablename__ = "dim_countries"

    country_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )