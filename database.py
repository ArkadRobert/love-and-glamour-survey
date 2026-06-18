import sqlite3

conn = sqlite3.connect("survey.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    rating TEXT,
    improvement TEXT,
    new_service TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully!")