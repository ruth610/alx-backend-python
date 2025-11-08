from datetime import time
import sqlite3

def log_queries(func):
    def wrapper(*args,**kwargs):
        start = time.time()
        print(f"calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"finished {func.__name__} in {time.time() - start:.2f}s")
        return result
    return wrapper
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

users = fetch_all_users(query="SELECT * FROM users")