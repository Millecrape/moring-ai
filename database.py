import sqlite3

def save_activity(task, description, decision):
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
        "INSERT INTO activities (task, description, decision) VALUES (?, ?, ?)",
        (task, description, decision)
    )

    conn.commit()
    conn.close()