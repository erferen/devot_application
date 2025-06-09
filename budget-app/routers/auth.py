from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from datetime import datetime, timedelta
from jose import jwt

from api_models.token import Token
from db.database import get_db
from api_models.user import UserCreate, UserResponse
from db.user import User
from db.category import Category
from constants import DEFAULT_CATEGORIES


router = APIRouter(tags=["Authentication"])

ph = PasswordHasher()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"


# --- JWT Token ---
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):

    decoded_name = jwt.decode(token, SECRET_KEY, algorithms=["HS256"]).get("sub")
    user = db.query(User).filter(User.username == decoded_name).one()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == form_data.username).one()
    user_schema = UserResponse.from_orm(db_user)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = ph.hash(form_data.password)
    if not ph.verify(hashed_password, form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token(data={"sub": user_schema.username})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_pw = ph.hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Add default categories for the new user
    for cat_name in DEFAULT_CATEGORIES:
        category = Category(name=cat_name, user_id=new_user.id)
        db.add(category)
    db.commit()

    token = create_access_token(data={"sub": new_user.username})
    return {"access_token": token, "token_type": "bearer"}