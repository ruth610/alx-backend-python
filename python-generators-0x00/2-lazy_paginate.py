import mysql.connector

def paginate_users(page_size, offset):
    """
    Fetches a single page of users from the database.
    """
    connection = mysql.connector.connect(
        host='localhost',
        user='root',        
        password='password',  
        database='ALX_prodev'
    )

    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


def lazy_paginate(page_size):
    """
    Generator that lazily fetches users page by page.
    """
    offset = 0
    while True:  # Loop 1
        page = paginate_users(page_size, offset)
        if not page:
            return  # Stop iteration if no more rows
        yield page
        offset += page_size


if __name__ == "__main__":
    for page in lazy_paginate(page_size=2):
        print("Page:")
        for user in page:
            print(user['name'], user['age'])
