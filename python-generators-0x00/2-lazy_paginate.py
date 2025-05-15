import mysql.connector

def connect_to_prodev():
    return mysql.connector.connect(
        host='localhost',
        user='your_mysql_user',
        password='your_mysql_password',
        database='ALX_prodev'
    )

def paginate_users(page_size, offset):
    """Fetches a single page of users starting at the given offset."""
    conn = connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def lazy_paginate(page_size):
    """Generator that lazily fetches users one page at a time."""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

# Example usage
if __name__ == "__main__":
    for page in lazy_paginate(3):
        for user in page:
            print(user)
# This code connects to a MySQL database, fetches user data in pages of a specified size,