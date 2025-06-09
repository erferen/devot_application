from pydantic import BaseModel
from typing import Optional
from datetime import date


class UserBase(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
        from_attributes = True


class UserCreate(UserBase):
    email: Optional[str]
    birth_date: Optional[date] 


class UserLogin(UserBase):
    pass


class UserResponse(BaseModel):

    username: str
    account_balance: float

    class Config:
        orm_mode = True
        from_attributes = True