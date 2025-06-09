from datetime import date

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from db.user import Base


class Bill(Base):
    __tablename__ = "bills"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    create_date: Mapped[date] = mapped_column(default=func.current_date(), nullable=False)

    # Foreign key to link to Category
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    # Many-to-one relationship with Category
    category: Mapped["Category"] = relationship(back_populates="bills")
    # Foreign key to link to User
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # Many-to-one relationship with User
    user: Mapped["User"] = relationship(back_populates="bills")