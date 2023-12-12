from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    String,
    DateTime,
    func,
    ARRAY,
    Integer,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ENUM as Enum
from sqlalchemy.orm import Mapped, mapped_column

from tgbot.services.film_api.models.films import FilmType

from .base import Base


class Film(Base):
    __tablename__ = "films"

    film_id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    name_ru: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    name_en: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    type: Mapped[FilmType] = mapped_column(
        Enum(FilmType, create_type=False), nullable=True
    )
    year: Mapped[Optional[int]] = mapped_column(Integer(), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    film_length: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    countries: Mapped[List[str]] = mapped_column(ARRAY(String()), nullable=True)
    genres: Mapped[List[str]] = mapped_column(ARRAY(String()), nullable=True)
    rating: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    rating_vote_count: Mapped[Optional[int]] = mapped_column(Integer(), nullable=True)
    poster_url: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    poster_url_preview: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    created_on: Mapped[datetime] = mapped_column(DateTime(), default=func.now())
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(), default=func.now(), onupdate=func.now()
    )


class Source(Base):
    __tablename__ = "sources"
    __table_args__ = (UniqueConstraint("film_id", "title", name="unique_source"),)

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    title: Mapped[str] = mapped_column(String(), nullable=False)
    url: Mapped[str] = mapped_column(String(), nullable=False)
    film_id: Mapped[int] = mapped_column(
        ForeignKey(Film.film_id, ondelete="CASCADE"), nullable=False
    )
    created_on: Mapped[datetime] = mapped_column(DateTime(), default=func.now())
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(), default=func.now(), onupdate=func.now()
    )
