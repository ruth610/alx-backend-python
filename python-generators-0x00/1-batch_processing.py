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
    for row in cursor:  # Loop 1
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch

    cursor.close()
    connection.close()
    
    return  # Explicitly ends the generator


def batch_processing(batch_size):
    """
    Processes each batch and yields users over the age of 25.
    """
    for batch in stream_users_in_batches(batch_size):  # Loop 2
        filtered_users = [user for user in batch if user['age'] > 25]  # Loop 3
        if filtered_users:
            yield filtered_users

    return  # Explicitly ends the generator


if __name__ == "__main__":
    for batch in batch_processing(batch_size=2):
        print("Filtered Batch:")
        for user in batch:
            print(user['name'], user['age'])
