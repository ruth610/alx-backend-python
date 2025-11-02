# alx-backend-python# ALX ProDev Database Seeder

This Python project sets up a MySQL database called `ALX_prodev` and populates it with sample user data from a CSV file (`user_data.csv`). It creates a table `user_data` with proper fields and handles duplicate entries gracefully.

---

## Features

- Connects to a MySQL server.
- Creates a database `ALX_prodev` if it doesn't exist.
- Creates a table `user_data` with the following fields:
  - `user_id` (UUID, Primary Key, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)
- Reads sample data from a CSV file.
- Inserts new records while avoiding duplicates based on email.
- Automatically generates UUIDs for new users.

---

## Requirements

- Python 3.8+
- MySQL Server
- Python Packages:
  - `mysql-connector-python`
  - `pandas`

Install dependencies with:

```bash
pip install mysql-connector-python pandas
