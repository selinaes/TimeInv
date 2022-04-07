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


def product_sort(conn, by, order):
    """
    Returns a list of all products sorted in ascending or descending order
    """
    curs = dbi.dict_cursor(conn)
    sql = "select * from product order by " + by +  " " + order
    curs.execute(sql)
    results = curs.fetchall()
    return results


def product_search(conn, search_type, query):
    curs = dbi.dict_cursor(conn)
    sql = """select * from product 
    where """ + search_type + """ like %s order by title"""
    curs.execute(sql, ['%' + query + '%'])
    results = curs.fetchall()
    return results


def products_addedby(conn, staff):
    curs = dbi.dict_cursor(conn)
    sql = """select * from product where 
    last_modified_by = %s"""
    curs.execute(sql, [staff])
    results = curs.fetchall()
    return results
