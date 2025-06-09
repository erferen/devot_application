from fastapi import APIRouter, Depends
from typing import Annotated
from routers.auth import get_current_user
from sqlalchemy.orm import Session
from db.database import get_db
from db.user import User
from api_models.user import UserResponse

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/info")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return UserResponse.from_orm(current_user)


@router.post("/add_balance")
async def add_balance(
    amount: float,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    if amount <= 0:
        return {"error": "Amount must be greater than zero"}
    current_user.account_balance += amount
    db.commit()
    db.refresh(current_user)
    return {"message": f"Balance updated. New balance: {current_user.account_balance}"}
