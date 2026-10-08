
import os
import psycopg
from datetime import datetime
from zoneinfo import ZoneInfo


def get_connection():
    database_url = os.environ.get("NEON_DATABASE_URL")

    if not database_url:
        import streamlit as st
        database_url = st.secrets["NEON_DATABASE_URL"]

    return psycopg.connect(database_url)


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS activities (
                    id SERIAL PRIMARY KEY,
                    task TEXT,
                    description TEXT,
                    decision TEXT,
                    result TEXT,
                    satisfaction INTEGER,
                    created_at DATE
                )
            """)


def save_activity(task, description, decision, result=None, satisfaction=None):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO activities
                (task, description, decision, result, satisfaction, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    task,
                    description,
                    decision,
                    result,
                    satisfaction,
                    datetime.now(ZoneInfo("Asia/Tokyo")).date()
                )
            )


def get_activities(limit=5):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT created_at, task, description, decision, result, satisfaction
                FROM activities
                ORDER BY created_at DESC, id DESC
                LIMIT %s
            """, (limit,))

            return cursor.fetchall()