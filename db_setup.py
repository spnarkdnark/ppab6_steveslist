import sqlite3 as sq
from os import path, remove


db_file_path = r'C:\Users\Samuel\PycharmProjects\i_be_learnin\steveslist\db_path'

with open(db_file_path, 'r') as file_object:
    db_path = file_object.read()


def db_exists(filepath):
    """
    Check if the database already exists.  Return True if so.
    :param filepath: Name of filepath to check
    :return: True if filepath exists
    """

    return path.exists(filepath)


def count_users(filepath):
    """
    Count how many rows exist in the users table database
    :return: integer of how many users exist
    """
    sql = """SELECT COUNT(*) FROM users"""
    conn = create_connection(filepath)
    c = conn.cursor()
    c.execute(sql)
    count = c.fetchone()

    return count[0]


def check_delete(filepath):
    """
    Check if the user wants to delete the current database.  Delete it if so.
    """
    count = count_users(filepath)
    check = input("Would you like to delete the database? There are currently " + str(count) + " users!")

    if check == 'yes':
        remove(filepath)
        create_db(filepath)
        print("Database wiped, new database created!")


def create_connection(filepath):
    """
    Create a connection to the requested database, returning the connection object used to manipulate said DB
    :param filepath: path to database
    :return: sqlite database connection object
    """

    conn = None

    try:
        # Connect to the database object and print current sqlite3 version, throw error if it fails
        conn = sq.connect(filepath)
        print(sq.version)
        return conn
    except sq.Error as e:
        print(e)

    return conn


def create_table(connection, statement):
    """
    Create a table inside of the selected database object
    :param connection: connection object, pointing toward appropriate database
    :param statement: statement used to create table
    """

    try:
        # Use a connection cursor to create a table in the database
        c = connection.cursor()
        c.execute(statement)
    except sq.Error as e:
        print(e)


def create_db(filepath):
    """
    Create a new database and add in a table for users
    :param filepath: filepath where database should be created
    """

    # Database statement being used with create_table function
    sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                    username text,
                                    password_hash text
                                    );
                             """
    # Create connection object from database filepath
    conn = sq.connect(filepath)

    # If connection succeeds, create the table
    if conn is not None:
        create_table(conn, sql_create_users_table)

    # If fails, print error
    else:
        print("Error! Trouble connecting to Database!")


if __name__ == "__main__":
    if db_exists(db_path):
        check_delete(db_path)
    else:
        create_db(db_path)