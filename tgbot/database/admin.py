from datetime import datetime
from sqlalchemy import String, DateTime, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Player(Base):
    __tablename__ = "players"

    title: Mapped[str] = mapped_column(String(), primary_key=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)
    created_on: Mapped[datetime] = mapped_column(DateTime(), default=func.now())
    updated_on: Mapped[datetime] = mapped_column(DateTime(), default=func.now(), onupdate=func.now())
