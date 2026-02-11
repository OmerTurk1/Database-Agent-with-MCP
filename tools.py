import sqlite3

def get_db_connection():
    return sqlite3.connect("database.db")

def show_tables():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        conn.commit()
        return cursor.fetchall()

def table_info(table_name: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        conn.commit()
        return cursor.fetchall()

def execute_query(command: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"{command}")
        conn.commit()
        return cursor.fetchall()