from functools import wraps
import logging

import mysql


def with_db_connection (config_db):
    """Decorator for MySQL connections."""
    def decorator(func):
        @wraps
        def wrapper(*args,**kwargs):
            conn = mysql.connector.connect(**config_db)
            try:
                result = func(conn,*args,**kwargs)
                conn.commit()
                return result
            except Exception as e:
                conn.rollback()
                print(f"Error: {e}")
                raise
            finally:
                conn.close()
        return wrapper
    return decorator
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "mypassword",
    "database": "mydb"
}

@with_db_connection(db_config)
def fetch_users(conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()
print(fetch_users())


        

    