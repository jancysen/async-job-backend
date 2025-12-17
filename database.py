import sqlite3

DB_NAME = "jobs.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            job_type TEXT,
            status TEXT,
            retries INTEGER,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()
