import sqlite3

def init_db():
    conn = sqlite3.connect("morning_ai.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            description TEXT,
            decision TEXT,
            result TEXT,
            satisfaction INTEGER,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()

def save_activity(task, description, decision, result=None, satisfaction=None):
    conn = sqlite3.connect("morning_ai.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO activities
        (task, description, decision, result, satisfaction, created_at)
        VALUES (?, ?, ?, ?, ?, date('now', 'localtime'))
        """,
        (task, description, decision, result, satisfaction)
    )

    conn.commit()
    conn.close()


def get_activities(limit=5):
    conn = sqlite3.connect("morning_ai.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT created_at, task, description, decision, result, satisfaction
        FROM activities
        ORDER BY created_at DESC, id DESC
        LIMIT ?
    """, (limit,))

    activities = cursor.fetchall()

    conn.close()
    return activities