# =================================================================================
#  Helper functions for the manage users page in app.py
#  Authors: Francisca Moya Jimenez, Jiawei Liu, Candice Ye, and Diana Hernandez
# =================================================================================

import cs304dbi as dbi


def get_all_access(conn, username):
    """
    Returns all users in the current db except from the user with the 
    given username
    Parameters:
        conn: a connection object
        username (string): a given username
    Returns:
        A list of dictionaries, where each dictionary represents
        a user
    """
    curs = dbi.dict_cursor(conn)
    sql = "select * from staff where username <> %s order by username"
    curs.execute(sql, [username])
    results = curs.fetchall()
    return results


def remove_member(conn, username):
    """
    Removes a member from the staff table given a username
    Parameters:
        conn: a connection object
        username (string): a username from the staff table
    Returns:
        None
    """
    curs = dbi.dict_cursor(conn)
    sql = "delete from staff where username = %s"
    curs.execute(sql, [username])
    conn.commit()

def edit_member(conn, username, name, role, permission):
    """
    Remove a member from the staff table given a username
    Parameters:
        conn: a connection object
        username (string): a username from the staff table
        name (string): the user's name
        name (role): the user's role
        name (permission): the user's permission
    Returns:
        A dictionary type object with the updated member information
    """
    curs = dbi.dict_cursor(conn)
    sql = "update staff set name =  %s, role = %s, permission = %s where username = %s"
    curs.execute("start transaction")
    curs.execute(sql, [name, role, permission, username])
    sql2 = "select * from staff where username = %s"
    curs.execute(sql2, [username])
    result = curs.fetchone()
    curs.execute("commit")
    conn.commit()
    return result


def add_member(conn, username, name, role, permission):
    """
    Add a member from the staff table given a username
    Parameters:
        conn: a connection object
        username (string): a username from the staff table
        name (string): the user's name
        name (role): the user's role
        name (permission): the user's permission
    Returns:
        A dictionary type object with the new member information
    """
    curs = dbi.dict_cursor(conn)
    sql = "insert into staff (username, name, role, permission) values (%s, %s, %s, %s)"
    curs.execute("start transaction")
    curs.execute(sql, [username, name, role, permission])
    sql2 = "select * from staff where username = %s"
    curs.execute(sql2, [username])
    result = curs.fetchone()
    curs.execute("commit")
    conn.commit()
    return result
