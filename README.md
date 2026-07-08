# Start database
cd file_manager_app>sqlite3 my_database.db  

# Start app
uvicorn main:app --reload  

# Open docs
open http://localhost:8000/docs#/  