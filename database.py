import sqlite3

def get_connection():
    return sqlite3.connect("nutrition.db", check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()

    # User table with role support
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        name TEXT,
        role TEXT DEFAULT 'student'
    )
    """)

    # Topics table with global flag for admin content
    c.execute("""
    CREATE TABLE IF NOT EXISTS topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        country TEXT,
        topic TEXT,
        content TEXT,
        is_global INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()