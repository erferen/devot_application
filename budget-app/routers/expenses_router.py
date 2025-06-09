from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated, Optional
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from db.database import get_db
from db.user import User
from db.bill import Bill
from routers.auth import get_current_user

router = APIRouter(prefix="/expenses", tags=["Expenses"])


class ExpenseCreate(BaseModel):
    # user_id: int
    amount: float
    description: str
    category_id: int
    create_date: date


class ExpenseUpdate(BaseModel):
    amount: float
    description: str
    create_date: Optional[date]

@router.post("/")
def create_expense(expense: ExpenseCreate, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    if expense.amount > current_user.account_balance:
        raise HTTPException(status_code=400, detail="Insufficient account balance")
    new_expense = Bill(
                       user_id=current_user.id,
                       amount=expense.amount,
                       description=expense.description,
                       create_date=expense.create_date,
                       category_id=expense.category_id
                       )
    db.add(new_expense)
    current_user.account_balance -= expense.amount
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.get("/{bill_id}")
def read_expense(bill_id: int, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    expense = db.query(Bill).filter(Bill.id == bill_id, Bill.user_id == current_user.id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.get("/")
def filter_expenses(
    current_user: Annotated[User, Depends(get_current_user)], 
    db: Session = Depends(get_db),
    category_name: str = None,  # Optional category filter
    create_date: date = None,  # Optional date filter
    price_min: float = None,
    price_max: float = None,
):

    query = db.query(Bill).filter(Bill.user_id == current_user.id)
    if category_name is not None:
        query = query.filter(Bill.category.has(name=category_name))
    if create_date is not None:
        query = query.filter(Bill.create_date == create_date)
    if price_min is not None:
        query = query.filter(Bill.amount >= price_min)
    if price_max is not None:
        query = query.filter(Bill.amount <= price_max)
    results = query.all()

    if not results:
        raise HTTPException(status_code=404, detail="No expenses found with given filters")
    return results


@router.put("/{bill_id}")
def update_expense(bill_id: int, expense_data: ExpenseUpdate, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    expense = db.query(Bill).filter(Bill.id == bill_id, Bill.user_id == current_user.id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense for current user not found")
    
    current_user.account_balance += expense.amount  # Revert old expense amount
    expense.amount = expense_data.amount
    expense.description = expense_data.description
    if expense_data.create_date:
        expense.create_date = expense_data.create_date
    current_user.account_balance -= expense.amount  # Deduct new expense amount
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{bill_id}")
def delete_expense(bill_id: int, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    
    expense = db.query(Bill).filter(Bill.id == bill_id, Bill.user_id == current_user.id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense for current user not found")
    current_user.account_balance += expense.amount  # Revert expense amount
    db.delete(expense)
    db.commit()
    return {"detail": "Expense deleted successfully"}


@router.get("/statistics/aggregate")
def aggregate_expenses(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    today = date.today()
    start_month = today.replace(day=1)
    start_quarter = today.replace(month=3*((today.month-1)//3)+1, day=1)
    start_year = today.replace(month=1, day=1)
    
    def sum_spent(start_date):
        return db.query(func.coalesce(func.sum(Bill.amount), 0)).filter(
            Bill.user_id == current_user.id,
            Bill.create_date >= start_date,
            Bill.create_date <= today
        ).scalar()

    spent_month = sum_spent(start_month)
    spent_quarter = sum_spent(start_quarter)
    spent_year = sum_spent(start_year)

    return {
        "spent_this_month": spent_month,
        "spent_this_quarter": spent_quarter,
        "spent_this_year": spent_year
    }