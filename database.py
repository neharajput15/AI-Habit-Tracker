import sqlite3

def get_connection():
    return sqlite3.connect("habit_tracker.db")

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
CREATE TABLE IF NOT EXISTS progress(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER NOT NULL,
    completed_date TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    FOREIGN KEY(habit_id) REFERENCES habits(id)
)
""")

    conn.commit()
    conn.close()

create_tables()