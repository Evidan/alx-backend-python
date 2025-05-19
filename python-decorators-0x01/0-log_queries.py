from datetime import datetime
import sqlite3
import functools

# Decorator to log SQL queries with a timestamp
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract SQL query
        query = kwargs.get('query', args[0] if args else None)
        if query:
            print(f"[{datetime.now()}] Executing SQL query: {query}")
        else:
            print(f"[{datetime.now()}] No SQL query found to log.")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
