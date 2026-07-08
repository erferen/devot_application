from sqlalchemy import create_engine

from db.database import Base, DATABASE_URL
from db import file, folder  # noqa: F401

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create all tables
try:
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")
except Exception as e:
    print(f"An error occurred while initializing the database: {e}")
