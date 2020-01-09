from add_user import get_hash_256
from db_setup import create_connection


error_message = "Argh matey, ye won't be finding any of my secret dubloons! ar hahahaha!"


db_file_path = r'C:\Users\Samuel\PycharmProjects\i_be_learnin\steveslist\db_path'

with open(db_file_path, 'r') as file_object:
    db_path = file_object.read()


def is_valid_credentials(filepath, username, password):
    """
    Check username and password against full list of credentials
    :param credentials: A dictionary of stored credentials
    :param username: given username
    :param password: given password
    :return: True if username and password exist correctly in Credentials dict
    """
    sql = """SELECT * FROM users WHERE username = ? and password_hash = ?"""
    conn = create_connection(filepath)
    c = conn.cursor()
    c.execute(sql, (username, password))
    exists = c.fetchall()

    return True if len(exists) is not 0 else False


def fetch_secret(filepath, username, password):
    """
    Fetches a great secret from the database corresponding to its user
    :return: A great secret
    """
    sql = """Select great_secret FROM users WHERE username = ? and password_hash = ?"""
    conn = create_connection(filepath)
    c = conn.cursor()
    c.execute(sql, (username, password))
    secret = c.fetchone()

    return secret[0]


def get_credentials():
    """
    get the user's credentials from the terminal
    :return: a username, password tuple
    """
    username = input('Please enter your username')
    password = input('Please enter your password')

    password_hash = get_hash_256(password)

    return username, password_hash


def run_login(filepath):
    """
    Run the login process, print appropriate message based on given credentials
    """
    credentials = get_credentials()
    if is_valid_credentials(filepath, credentials[0], credentials[1]):
        great_secret = fetch_secret(filepath, credentials[0], credentials[1])
        print(great_secret)
    else:
        print(error_message)


if __name__ == "__main__":
    run_login(db_path)