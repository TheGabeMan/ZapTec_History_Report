import sqlite3
from datetime import datetime, timedelta
# from sqlite3.dbapi2 import Cursor


def sql_connect():
    # Connect to a database (creates one if it doesn't exist)
    conn = sqlite3.connect('chargehistory.db')
    cursor = conn.cursor()
    return conn, cursor


def sql_createtable(conn, cursor):
    # Create a table
    # TEXT as ISO8601 strings (“YYYY-MM-DD HH:MM:SS.SSS”).
    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            "UserUserName"	TEXT NOT NULL,
            "Id"	TEXT NOT NULL,
            "DeviceID"	TEXT,
            "StartDateTime"	INT NOT NULL,
            "EndDateTime"	INT NOT NULL,
            "Energy"	INTEGER NOT NULL,
            "UserFullName"	TEXT,
            "ChargerId"	TEXT,
            "DeviceName"	TEXT,
            "UserEmail"	TEXT,
            "UserId"	TEXT,
            PRIMARY KEY("StartDateTime")
        )''')
        conn.commit()
        return True
    except sqlite3.Error as err:
        conn.rollback()
        print(f"An error occurred: {err}")
        return False


def sql_insert(key):
    # Store data into sqlite
    # Check db connection
    conn, cursor = sql_connect()

    # Create Tabel if not exists
    if not sql_createtable(conn=conn, cursor=cursor):
        print('Error creating table')

    # Single insertion
    try:
        # StartDate, EndDate TEXT as ISO8601 strings (“YYYY-MM-DD HH:MM:SS.SSS”).
        # UnixStartDateTime = datetime.fromisoformat(key['StartDateTime']).timestamp()
        UnixStartDateTime = datetime.strptime(key['StartDateTime'], '%Y-%m-%dT%H:%M:%S.%f').timestamp()
        UnixEndDateTime = datetime.strptime(key['EndDateTime'], '%Y-%m-%dT%H:%M:%S.%f').timestamp()

        cursor.execute('''
        INSERT INTO sessions (
        "UserUserName",
        "Id",
        "DeviceID",
        "StartDateTime",
        "EndDateTime",
        "Energy",
        "UserFullName",
        "ChargerId",
        "DeviceName",
        "UserEmail",
        "UserId"        ) 
        VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''',
            (
                key['UserUserName'],
                key['Id'],
                key['DeviceId'],
                UnixStartDateTime,
                UnixEndDateTime,
                key['Energy'],
                key['UserFullName'],
                key['ChargerId'],
                key['DeviceName'],
                key['UserEmail'],
                key['UserId']
            ))
        conn.commit()
        return False
    except sqlite3.Error as err:
        conn.rollback()
        print(f"An error occurred: {err}")
        return True


# def sql_query():
#     # Simple select
#     cursor.execute('SELECT * FROM users')
#     print(cursor.fetchall())

#     # Parameterized query
#     cursor.execute('SELECT * FROM users WHERE age > ?', (25,))
#     print(cursor.fetchall())

#     # Fetching with column names
#     cursor.execute('SELECT * FROM users')
#     # Get column names
#     columns = [column[0] for column in cursor.description]
#     # Fetch rows as dictionaries
#     rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
#     print(rows)


def sql_context_manager():
    import sqlite3

    # Automatically handles connection closing
    with sqlite3.connect('example.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('YOUR QUERY')
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            print(f"An error occurred: {e}")


def sql_transaction():
    # Transactions
    conn.execute('BEGIN TRANSACTION')
    try:
        # Multiple operations
        cursor.execute('UPDATE users SET age = age + 1')
        cursor.execute('INSERT INTO logs (action) VALUES ("age update")')
        conn.commit()
    except sqlite3.Error:
        conn.rollback()


def insert_user(username, email, age):
    # Practical example with error handling
    try:
        with sqlite3.connect('example.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO users (username, email, age) 
            VALUES (?, ?, ?)
            ''', (username, email, age))
            return cursor.lastrowid  # Returns the ID of the last inserted row
    except sqlite3.IntegrityError:
        print("Username already exists")
        return None


