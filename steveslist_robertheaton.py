import sqlite3 as sq
import hashlib


my_great_secret = "Yargh, The dubloons are buried fourty paces east of your nearest 7/11"

error_message = "Argh matey, ye won't be finding any of my secret dubloons! ar hahahaha!"


def add_user_sql(conn, user_info):

    sql = '''INSERT into users(username, password_hash) VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, user_info)


def add_user(filepath):

    username = input("Please enter your username")
    password = input("Please enter your password")

    password_hash = get_hash_256(password)

    conn = create_connection(filepath)

    with conn:
        add_user_sql(conn, (username, password_hash))


def is_valid_credentials(credentials, username, password):
    """
    Check username and password against full list of credentials
    :param credentials: A dictionary of stored credentials
    :param username: given username
    :param password: given password
    :return: True if username and password exist correctly in Credentials dict
    """
    for userpass in credentials:
        if userpass.get(username) == password:
            return True


def get_credentials():
    """
    get the user's credentials from the terminal
    :return: a username, password tuple
    """
    username = input('Please enter your username')
    password = input('Please enter your password')

    return username, password


def get_hash_256(pass_to_hash):
    """
    return a hash of the password
    :param pass_to_hash: password to be hashed
    :return: the hashed password value
    """
    hashed_pass = hashlib.sha256(str.encode(pass_to_hash)).hexdigest()
    return hashed_pass


def run_login(repo_filepath):
    """
    Run the login process, print appropriate message based on given credentials
    """
    credentials = get_credentials()
    repo = get_json_data(repo_filepath)
    if is_valid_credentials(repo, credentials[0], credentials[1]):
        print(my_great_secret)
    else:
        print(error_message)



create_db(db_path)
add_user(db_path)