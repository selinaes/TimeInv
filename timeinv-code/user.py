# =================================================================================
#  Helper functions for login and signup pages in app.py
#  Authors: Francisca Moya Jimenez, Jiawei Liu, Candice Ye, and Diana Hernandez
# =================================================================================

import cs304dbi as dbi
import user
from flask import session
import exceptions

def set_login_info(conn, username):
    """
    Sets a user information in the current session before logging in

    Parameters:
        conn: a connection object
        username (string): a username 

    Returns:
        None
    """
    session['username'] = username
    session['logged_in'] = True
    permissions = user.get_permissions(conn, username)
    session['permissions'] = permissions.get('permission')

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
        raise exceptions.UsernameFormatError()
    sql = "select * from staff where username = %s"
    sql1 = "insert into userpass (username, hashed) values (%s, %s)"
    # Start transaction to make sure that user is able to complete
    # entire signup process atomically   
    curs.execute("start transaction")
    curs.execute(sql, [username])
    result = curs.fetchall()
    if len(result) == 0:
        # Rollback transaction if username does not exist. Raise an error that 
        # is catched on the page and shown to the user
        curs.execute("rollback")
        raise exceptions.UsernameNonExistent()
    curs.execute(sql1, [username, hashed])
    curs.execute("commit")
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

def get_permissions(conn, username):
    """
    Returns permissions for a given user

    Parameters:
        conn: a connection object
        username (string): a username

    Returns:
        A dictionary type object with the permissions for a username
    """
    curs = dbi.dict_cursor(conn)
    sql = "select permission from staff where username =  %s"
    curs.execute(sql, [username])
    results = curs.fetchone()
    return results