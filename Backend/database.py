import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="waste_management"
)

print("Database Connected Successfully")
