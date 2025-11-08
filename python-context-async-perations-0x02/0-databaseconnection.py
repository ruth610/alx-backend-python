import mysql.connector
from mysql.connector import cursor

class DatabaseConnection :
    def __init__(self,host,user,password,database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None
    def __enter__(self):
        self.conn = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database

        )
        self.cursor = self.conn.cursor(dictionary=True)
        return self.cursor
    def __exit__(self,exc_type,exc_value,traceback):
        if exc_type:
            print(f"exception occurred {exc_type},{exc_value}")
        else:
            self.conn.rollback()
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        return False

if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "root",
        "database": "laravel"
    }
    with DatabaseConnection(**db_config) as cursor:
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
