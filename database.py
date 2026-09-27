import sqlite3

def save_activity(task, description, decision, created_at):
    conn = sqlite3.connect("morning_ai.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        description TEXT,
        decision TEXT,
        result TEXT,
        satisfaction INTEGER,
        created_at TEXT
    )
    """)

    cursor.execute(
        "INSERT INTO activities (task, description, decision, created_at) VALUES (?, ?, ?, ?)",
        (task, description, decision, created_at)
    )

    conn.commit()
    conn.close()

def get_activities():
    conn = sqlite3.connect("morning_ai.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT created_at, description, result
        FROM activities
        ORDER BY created_at DESC
    """)

    activities = cursor.fetchall()

    conn.close()
    return activities