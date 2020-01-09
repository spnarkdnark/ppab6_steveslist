from db_setup import create_connection
import hashlib


db_file_path = r'C:\Users\Samuel\PycharmProjects\i_be_learnin\steveslist\db_path'

with open(db_file_path, 'r') as file_object:
    db_path = file_object.read()


def get_hash_256(pass_to_hash):
    """
    return a hash of the password
    :param pass_to_hash: password to be hashed
    :return: the hashed password value
    """

    hashed_pass = hashlib.sha256(str.encode(pass_to_hash)).hexdigest()
    return hashed_pass


def check_user_exists(username, conn):
    """
    Check if a username already exists in given database
    :param username: Username to query against the database
    :param conn: connection object used to create cursor
    :return: True if username already exists
    """

    cur = conn.cursor()
    cur.execute("SELECT username FROM users WHERE username = ?", [username])
    user = cur.fetchall()

    if len(user) == 0:
        return True
    else:
        return False


def add_user(filepath):
    """
    Adds a user, password and great secret to the database, checking if the user already exists first
    :param filepath:
    """
    adding = True
    conn = create_connection(filepath)

    while adding:
        username = input("Please enter your username")
        if check_user_exists(username, conn):
            adding = False
        else:
            print("Please select a different username!")

    password = input("Please enter your password")
    password_hash = get_hash_256(password)

    great_secret = input("What is your great secret?")

    with conn:
        add_user_sql(conn, (username, password_hash, great_secret))


def add_user_sql(conn, user_info):
    """
    The SQL utility function used to add a user to the database
    :param conn: Connection object
    :param user_info: username, password hash and great secret
    :return:
    """
    sql = '''INSERT into users(username, password_hash, great_secret) VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, user_info)


if __name__ == "__main__":
    add_user(db_path)