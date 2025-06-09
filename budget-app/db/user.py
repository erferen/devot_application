from typing import Optional
from datetime import date

from sqlalchemy import String, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    hashed_password: Mapped[str]
    account_balance: Mapped[Optional[float]] = mapped_column(Float, default=10000.0)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    birth_date: Mapped[Optional[date]] = mapped_column(nullable=True)

    # One-to-many relationship with Bill
    bills: Mapped[list["Bill"]] = relationship(back_populates="user")
    # One-to-many relationship with Category
    categories: Mapped[list["Category"]] = relationship(back_populates="user")