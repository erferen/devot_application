from sqlalchemy import create_engine
from db.user import Base, User
from db.bill import Bill
from db.category import Category
from db.database import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create all tables
try:
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")
except Exception as e:
    print(f"An error occurred while initializing the database: {e}")
