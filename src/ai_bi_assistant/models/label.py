from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ai_bi_assistant.models.base import Base


class Label(Base):
    __tablename__ = "dim_labels"

    label_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    label: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )