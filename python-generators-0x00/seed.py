import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import uuid


CSV_FILE = 'user_data.csv'


def connect_db():
    """Connect to the MySQL server."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',        
            password='password'
        )
        print("Connected to MySQL server successfully.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Create the ALX_prodev database if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev is ready.")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',        # replace with your MySQL username
            password='password',# replace with your MySQL password
            database='ALX_prodev'
        )
        print("Connected to ALX_prodev database.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    """Create the user_data table if it does not exist."""
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) NOT NULL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(5,2) NOT NULL,
        UNIQUE KEY idx_user_id (user_id)
    )
    """
    try:
        cursor.execute(create_table_query)
        print("Table user_data is ready.")
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")
    finally:
        cursor.close()

def insert_data(connection, data):
    """Insert data into the user_data table if it does not exist."""
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """
    
    for _, row in data.iterrows():
        user_id = str(uuid.uuid4())  # generate a new UUID for each row
        name = row['name']
        email = row['email']
        age = row['age']
        
        # Check if email already exists
        cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
        if cursor.fetchone():
            print(f"User with email {email} already exists. Skipping...")
            continue
        
        cursor.execute(insert_query, (user_id, name, email, age))
        print(f"Inserted user: {name}")
    
    connection.commit()
    cursor.close()


# ---------- Main Script ----------
if __name__ == "__main__":
    # Load CSV data
    data = pd.read_csv(CSV_FILE)
    
    # Connect to MySQL server
    server_conn = connect_db()
    if server_conn:
        create_database(server_conn)
        server_conn.close()
    
    # Connect to ALX_prodev database
    db_conn = connect_to_prodev()
    if db_conn:
        create_table(db_conn)
        insert_data(db_conn, data)
        db_conn.close()
