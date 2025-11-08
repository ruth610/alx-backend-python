import mysql.connector
from mysql.connector import cursor

class ExecuteQuery:
    def __init__(self,host,database,password,user):
        self.host = host
        self.database =  database
        self.password = password
        self.user = user
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
    def __exit__(self,exc_type,exc_val,exc_bt):
        if exc_type:
            print(f"execution error occured{exc_type}: {exc_val}")
        else:
            self.conn.rollback()
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.cursor.close()
        return False
if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "root",
        "database": "laravel"
    }

    with ExecuteQuery(**db_config) as cursor:
        age = 25
        cursor.execute("SELECT * FROM users WHERE age > %s",(age,))
        rows = cursor.fetchall()
        for row in rows:
            print(row)

