# =================================================================================
#  Helper functions for login and signup pages in app.py
#  Authors: Francisca Moya Jimenez, Jiawei Liu, Candice Ye, and Diana Hernandez
# =================================================================================

import cs304dbi as dbi

def get_password_by_username(conn, username):
    """
    Returns the username and the hashed password for a given username.

    Parameters:
        conn: a connection object
        username (string): a username 

    Returns:
        None if the given username doesn't exist, and
        a dictionary-like object if the username exists
        with the username and the hashed password stored
    """
    curs = dbi.dict_cursor(conn)
    curs.execute("""SELECT username, hashed
                    FROM userpass
                    WHERE username = %s""",
                     [username])
    row = curs.fetchone()
    return row

def insert_new_account(conn, username, hashed):
    """
    Inserts a new user into the database using the given username and the hashed password.

    Parameters:
        conn: a connection object
        username (string): a username, must have a length less or equal to 10 characters
        hashed (string): a hashed password with a salt

    Returns:
        None
    """
    curs = dbi.cursor(conn)
    if len(username) > 10:
        raise Exception("Could not sign up user. The username must have at most 10 characters.")
    sql = "insert into userpass (username, hashed) values (%s, %s)"
    curs.execute(sql, [username, hashed])
    conn.commit()
    


def username_exists(conn, username):
    """
    Checks whether a username exists.

    Parameters:
        conn: a connection object
        username (string): a username

    Returns:
        true if the username exists and false if it doesn't
    """
    curs = dbi.dict_cursor(conn)
    sql = "select username from userpass where username =  %s"
    curs.execute(sql, [username])
    results = curs.fetchall()
    return len(results) > 0