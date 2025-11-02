import mysql.connector

def stream_user_ages():
    """
    Generator that yields user ages one by one from the database.
    """
    connection = mysql.connector.connect(
        host='localhost',
        user='root',         
        password='password',  
        database='ALX_prodev'
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:  # Loop 1
        yield row['age']

    cursor.close()
    connection.close()
    return  # explicitly stop the generator


def compute_average_age():
    """
    Computes the average age of users using the age generator.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():  # Loop 2
        total_age += age
        count += 1

    if count == 0:
        return 0
    return total_age / count

if __name__ == "__main__":
    average_age = compute_average_age()
    print(f"Average age of users: {average_age:.2f}")
