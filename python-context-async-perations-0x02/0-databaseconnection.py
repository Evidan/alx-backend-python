import sqlite3

# Custom context manager class
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn  # This is what gets assigned to `as` in the `with` statement

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()

# Use the context manager to perform a query
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
