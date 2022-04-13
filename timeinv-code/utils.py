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
    """
    Returns a list of all products that contain the query string
    """
    curs = dbi.dict_cursor(conn)
    sql = """select * from product 
    where """ + search_type + """ like %s order by title"""
    curs.execute(sql, ['%' + query + '%'])
    results = curs.fetchall()
    return results


def products_addedby(conn, staff):
    """
    Returns a list of all products that were added by a specific staff member
    """
    curs = dbi.dict_cursor(conn)
    sql = """select * from product where 
    last_modified_by = %s"""
    curs.execute(sql, [staff])
    results = curs.fetchall()
    return results

# def sku_exists(conn, sku):
#     """
#     Returns whether sku exists in the product list
#     """
#     curs = dbi.dict_cursor(conn)
#     sql = """select sku from product where 
#     sku = %s"""
#     curs.execute(sql, [sku])
#     results = curs.fetchall()
#     return len(results) > 0

# def sku_exists(conn, sku):
#     """
#     Returns whether sku exists in the product list
#     """
#     curs = dbi.dict_cursor(conn)
#     sql = """select sku from product where 
#     sku = %s"""
#     curs.execute(sql, [sku])
#     results = curs.fetchall()
#     return len(results) > 0

def update_product(conn, title, price, last_modified_by, sku):
    """
    Updates a product in the timeinv_db database without changes to sku
    """
    curs = dbi.dict_cursor(conn)
    sql = """update product 
    set title = %s, price = %s, last_modified_by = %s
    where sku = %s"""
    curs.execute(sql, [sku, title, price, last_modified_by])
    conn.commit()


def get_all_transactions(conn):
    """
    Returns all transactions in the current db
    """
    curs = dbi.dict_cursor(conn)
    sql = "select sku, title, timestamp, sum(amount) from product, transaction using (sku) group by sku order by timestamp, sku"
    curs.execute(sql)
    results = curs.fetchall()
    return results

def transaction_sort(conn, by, order):
    curs = dbi.dict_cursor(conn)
    # Prepared queries can only be used for values, not column names or order
    sql = "select sku, title, timestamp, sum(amount) from product, transaction using (sku) group by sku " + by +  " " + order
    curs.execute(sql)
    results = curs.fetchall()
    return results


def transaction_search(conn, search_type, query):
    """
    Returns a list of all products that contain the query string
    """
    curs = dbi.dict_cursor(conn)
    sql = """select sku, title, timestamp, sum(amount) from product, transaction using (sku) group by sku
    where """ + search_type + """ like %s order by title"""
    curs.execute(sql, ['%' + query + '%'])
    results = curs.fetchall()
    return results

def sku_exists(conn, sku):
    """
    Returns whether sku exists in the product list
    """
    curs = dbi.dict_cursor(conn)
    sql = """select sku from transaction where 
    sku = %s"""
    curs.execute(sql, [sku])
    results = curs.fetchall()
    return len(results) > 0
    curs.execute(sql, [title, price, last_modified_by, sku])
    conn.commit()

def update_product_new_sku(conn, title, price, last_modified_by, og_sku, new_sku):
    """
    Updates a product in the timeinv_db database with a new sku
    """
    curs = dbi.dict_cursor(conn)
    sql = """update product 
    set sku = %s, title = %s, price = %s, last_modified_by = %s
    where sku = %s"""
    curs.execute(sql, [new_sku, title, price, last_modified_by, og_sku])
    conn.commit()
