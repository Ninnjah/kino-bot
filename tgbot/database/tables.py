from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, BigInteger, Boolean, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    def __repr__(self):
        params = {x: self.__getattribute__(x) for x in self.__dict__ if not x.startswith('_')}
        return self.__class__.__name__ + "(" + ", ".join(f"{key}={value}" for key, value in params.items()) + ")"


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
