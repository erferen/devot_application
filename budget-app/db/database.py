from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- Config ---
DATABASE_URL = "sqlite:///../my_database.db"
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- DB Setup ---
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# Create all tables in the database
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()