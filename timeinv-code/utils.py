# ==============================
#  Helpers functions for app.py
# ==============================

import cs304dbi as dbi


def get_all_products(conn):
    """
    Returns all products in the current db

    Parameters:
        conn: a connection object

    Returns:
        A list of dictionaries, where each dictionary is an object
    """
    curs = dbi.dict_cursor(conn)
    sql = "select * from product order by title"
    curs.execute(sql)
    results = curs.fetchall()
    return results
