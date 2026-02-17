import sqlite3
import os

print("Current directory:", os.getcwd())

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

cursor.execute("SELECT * FROM users;")
rows = cursor.fetchall()

print("\nUsers in DB:")
for row in rows:
    print(row)

conn.close()
