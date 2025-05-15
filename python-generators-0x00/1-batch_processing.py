import mysql.connector
import uuid

def connect_to_prodev():
    return mysql.connector.connect(
        host='localhost',
        user='your_mysql_user',
        password='your_mysql_password',
        database='ALX_prodev'
    )

def stream_users_in_batches(batch_size):
    """Yields user data in batches from the user_data table."""
    conn = connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) FROM user_data")
    total = cursor.fetchone()['COUNT(*)']

    for offset in range(0, total, batch_size):
        cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset))
        users = cursor.fetchall()
        if users:
            yield users

    cursor.close()
    conn.close()

def batch_processing(batch_size):
    """Processes each batch and yields users over the age of 25."""
    for batch in stream_users_in_batches(batch_size):
        yield [user for user in batch if user['age'] > 25]

# Example usage
if __name__ == "__main__":
    for users_over_25 in batch_processing(3):
        for user in users_over_25:
            print(user)
