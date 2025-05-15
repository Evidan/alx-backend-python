Overview
This script initializes and seeds a MySQL database named ALX_prodev with sample user data. It is part of the backend infrastructure for a larger system and sets up a user_data table, populating it from a CSV file (user_data.csv) using Python.

⚙️ Features
Connects to the MySQL server.

Creates the ALX_prodev database if it does not exist.

Creates the user_data table with the following schema:

user_id (UUID, Primary Key, Indexed)

name (VARCHAR, NOT NULL)

email (VARCHAR, NOT NULL)

age (DECIMAL, NOT NULL)

Reads and loads user data from user_data.csv.

Inserts data into the user_data table (avoiding duplicates).

📂 Files
seed.py – Python script that connects to MySQL, creates the database and table, and inserts data.

user_data.csv – CSV file with sample user data (columns: name, email, age).

