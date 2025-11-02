import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from user_data table in batches.
    Yields a list of dictionaries (one batch at a time).
    """
    connection = mysql.connector.connect(
        host='localhost',
        user='root',         
        password='password',
        database='ALX_prodev'
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    batch = []
    for row in cursor:  # Loop 1: iterate through all rows
        batch.append(row)
        if len(batch) == batch_size:
            yield batch  # Yield the full batch
            batch = []

    if batch:  # Yield remaining rows if any
        yield batch

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes each batch and yields users over the age of 25.
    """
    for batch in stream_users_in_batches(batch_size): 
        filtered_users = [user for user in batch if user['age'] > 25] 
        if filtered_users:
            yield filtered_users

if __name__ == "__main__":
    for batch in batch_processing(batch_size=2):
        print("Filtered Batch:")
        for user in batch:
            print(user['name'], user['age'])
