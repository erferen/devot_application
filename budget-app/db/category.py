from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db.user import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)

    # One-to-many relationship with Bill
    bills: Mapped[list["Bill"]] = relationship(back_populates="category")
    # Foreign key to link to User
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # Many-to-one relationship with User
    user: Mapped["User"] = relationship(back_populates="categories")