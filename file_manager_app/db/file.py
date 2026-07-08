from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base

if TYPE_CHECKING:
    from db.folder import Folder


class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    folder_id: Mapped[int] = mapped_column(
        ForeignKey("folders.id"), nullable=False
    )

    folder: Mapped["Folder"] = relationship(
        "Folder",
        back_populates="files",
    )
