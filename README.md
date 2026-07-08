# Initial setup
Have poetry installed (check with poetry --version)  
Run: <b>poetry install</b>
in project repo

# Start database
cd file_manager_app>sqlite3 my_database.db  

# Start app
uvicorn main:app --reload  

# Open docs
open http://localhost:8000/docs#/  