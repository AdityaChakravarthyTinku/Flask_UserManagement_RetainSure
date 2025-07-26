import sqlite3
from contextlib import contextmanager
# from .config import DB_NAME

def get_connection():
    return sqlite3.connect("users.db", check_same_thread=False)

@contextmanager
def get_cursor():
    """
    Context manager for cursor.
    Automatically commits or rolls back transactions.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def fetch_one(query, params=()):
    with get_cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchone()

def fetch_all(query, params=()):
    with get_cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()

# def execute_query(query, params=()):
#     with get_cursor() as cursor:
#         cursor.execute(query, params)
#         return cursor.rowcount

def execute_query(query, params=()):
    with get_cursor() as cursor:
        cursor.execute(query, params)
        # For INSERT or UPDATE or DELETE, rowcount can be -1 in SQLite
        # We can manually check changes using `SELECT changes();`
        cursor.execute("SELECT changes();")
        changes = cursor.fetchone()[0]
        return changes
