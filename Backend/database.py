import sqlite3

def get_db_connection():
    db = sqlite3.connect("waste_management.db", check_same_thread=False)
    db.row_factory = sqlite3.Row  # Column names use panna help pannum
    return db

db = get_db_connection()
print("Database Connected Successfully")