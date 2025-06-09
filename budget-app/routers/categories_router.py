from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List, Annotated
from db.database import get_db
from db.user import User
from db.category import Category
from routers.auth import get_current_user
from api_models.category import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Create a new category
@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    # new_category = Category(**category.model_dump())
    new_category = Category(name=category.name, user_id=current_user.id)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


# Read all categories
@router.get("/", response_model=List[CategoryResponse])
def get_categories(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    #categories = db.query(Category).all()
    categories =  db.query(Category).filter(Category.user_id == current_user.id).all()
    return categories


# Read a single category by ID
@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id, Category.user_id == current_user.id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


# Update a category
@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, updated_category: CategoryCreate, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id, Category.user_id == current_user.id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in updated_category.model_dump().items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category


# Delete a category
@router.delete("/{category_name}")
def delete_category(category_name: str, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.name == category_name, Category.user_id == current_user.id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"detail": f"Category {category_name} deleted successfully"}