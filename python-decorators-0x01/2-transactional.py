from functools import wraps
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

def transactional(func):
    @wraps
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn,*args,**kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"transaction failed: {e}")
            raise
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
    #### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='addis@gmail.com')

