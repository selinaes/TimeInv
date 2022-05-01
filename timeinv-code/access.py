# =================================================================================
#  Helper functions for the products page in app.py
#  Authors: Francisca Moya Jimenez, Jiawei Liu, Candice Ye, and Diana Hernandez
# =================================================================================

import cs304dbi as dbi


def get_all_access(conn):
    """
    Returns all users in the current db
    Parameters:
        conn: a connection object
    Returns:
        A list of dictionaries, where each dictionary represents
        a user
    """
    curs = dbi.dict_cursor(conn)
    sql = "select * from staff order by username"
    curs.execute(sql)
    results = curs.fetchall()
    return results


def remove_member(conn, username):
    """
    Remove a member from the staff table given a username
    Parameters:
        conn: a connection object
        username (string): a username from the staff table
    Returns:
        None
    """
    curs = dbi.dict_cursor(conn)
    print(username)
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
        The new member information
    """
    curs = dbi.dict_cursor(conn)
    print(username)
    sql = "update staff set name =  %s, role = %s, permission = %s where username = %s"
    curs.execute(sql, [name, role, permission, username])
    conn.commit()
    return ({'username': username, 'name': name, 'role': role, 
    'permission': permission})