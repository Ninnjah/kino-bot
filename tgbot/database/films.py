from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, DateTime, BigInteger, func, ARRAY, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Film(Base):
    __tablename__ = "films"

    film_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name_ru: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    name_en: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    year: Mapped[Optional[int]] = mapped_column(Integer(), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    film_length: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    countries: Mapped[List[str]] = mapped_column(ARRAY(String()), nullable=True)
    genres: Mapped[List[str]] = mapped_column(ARRAY(String()), nullable=True)
    rating: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    poster_url: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    created_on: Mapped[datetime] = mapped_column(DateTime(), default=func.now())
    updated_on: Mapped[datetime] = mapped_column(DateTime(), default=func.now(), onupdate=func.now())
