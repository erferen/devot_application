from pydantic import BaseModel


class FileBase(BaseModel):
    name: str
    folder_id: int


class FileCreate(FileBase):
    pass


class FileUpdate(FileBase):
    pass


class FileOut(FileBase):
    id: int

    class Config:
        from_attributes = True