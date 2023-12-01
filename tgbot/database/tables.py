from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, BigInteger, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    firstname: Mapped[str] = mapped_column(String(), nullable=False)
    lastname: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    username: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    created_on: Mapped[datetime] = mapped_column(DateTime(), default=func.now())
    updated_on: Mapped[datetime] = mapped_column(DateTime(), default=func.now(), onupdate=func.now())


class Admin(Base):
    __tablename__ = "admins"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_on: Mapped[datetime] = mapped_column(DateTime(), default=func.now())
    updated_on: Mapped[datetime] = mapped_column(DateTime(), default=func.now(), onupdate=func.now())
