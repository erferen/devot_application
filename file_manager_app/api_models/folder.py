
from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


class FolderBase(BaseModel):
	name: str = Field(..., min_length=1, max_length=255)


class FolderCreate(FolderBase):
	parent_id: Optional[int] = 0


class FolderUpdate(BaseModel):
	name: Optional[str] = Field(None, min_length=1, max_length=255)


class Folder(FolderBase):
	id: int
	parent_id: Optional[int] = 0

	class Config:
		from_attributes = True
