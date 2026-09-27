import sqlite3


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


def get_activities():
    conn = sqlite3.connect("morning_ai.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT created_at, task, description, decision, result, satisfaction
        FROM activities
        ORDER BY created_at DESC, id DESC
    """)

    activities = cursor.fetchall()

    conn.close()
    return activities