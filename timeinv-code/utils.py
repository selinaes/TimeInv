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

def product_insert(conn, sku, name, price, staff):
    curs = dbi.dict_cursor(conn)
    sql = """insert into product
    values (%s, %s, %s, %s, %s)"""
    curs.execute(sql, [sku, name, price, 
    staff, None]) 
    conn.commit()

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

def delete_product_by_sku(conn, sku):
    """
    Delets a product from the database given a sku
    """
    curs = dbi.dict_cursor(conn)
    sql = "delete from product where sku = %s"
    curs.execute(sql, [sku])
    conn.commit()

def get_products_below_threshold(conn, threshold):
    """
    Returns list of products below the given threshold
    """
    curs = dbi.dict_cursor(conn)
    sql = """select transaction.sku as sku, title, sum(amount) as total_amount from 
    transaction inner join product using (sku) group by sku having total_amount < %s
    """
    curs.execute(sql, [threshold])
    results = curs.fetchall()
    return results



def transaction_sort(conn, by, order):
    curs = dbi.dict_cursor(conn)
    # Prepared queries can only be used for values, not column names or order
    sql = "select sku, title, timestamp from product, transaction using (sku) " + by +  " " + order
    curs.execute(sql)
    results = curs.fetchall()
    return results

def transaction_search(conn, search_type, query):
    """
    Returns a list of all products that contain the query string
    """
    curs = dbi.dict_cursor(conn)
    sql = """select sku, title, timestamp from product, transaction using (sku) 
    where """ + search_type + """ like %s order by title"""
    curs.execute(sql, ['%' + query + '%'])
    results = curs.fetchall()
    return results