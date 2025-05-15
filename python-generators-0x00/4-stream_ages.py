import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="your_user",
        password="your_password",
        database="ALX_prodev"
    )

def stream_user_ages():
    """Generator that yields user ages one by one."""
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:
        yield age
    cursor.close()
    conn.close()

def calculate_average_age():
    """Calculates average age using the generator."""
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    average_age = total_age / count if count > 0 else 0
    print(f"Average age of users: {average_age:.2f}")

if __name__ == "__main__":
    calculate_average_age()
# This script connects to a MySQL database, retrieves user ages from the `user_data` table,
# and calculates the average age using a generator function.