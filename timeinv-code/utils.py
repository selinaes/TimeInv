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
    values (%s, %s, %s, %s, %s, %s)"""
    curs.execute(sql, [sku, name, price, 0, 
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


def update_product(conn, title, price, last_modified_by, sku):
    """
    Updates a product in the timeinv_db database without changes to sku
    """
    curs = dbi.dict_cursor(conn)
    sql = """update product 
    set title = %s, price = %s, last_modified_by = %s
    where sku = %s"""
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

def inventory_below_threshold(conn, threshold):
    """
    Returns list of products below the given threshold
    """
    curs = dbi.dict_cursor(conn)
    sql = """select sku, title, max(timestamp) as latesttime, sum(amount) as inventory from 
    transaction inner join product using (sku) group by sku having inventory < %s
    """
    curs.execute(sql, [threshold])
    results = curs.fetchall()
    return results


def inventory_by_sku(conn, sku):
    """
    Returns the requested sku product and its inventory information
    """
    curs = dbi.dict_cursor(conn)
    sql = """SELECT sku, title, max(timestamp) as latesttime, sum(amount) as inventory 
    FROM product INNER JOIN transaction 
    USING (sku) 
    WHERE sku = %s
    """
    curs.execute(sql, [sku])
    results = curs.fetchall()
    print(results)
    return results

def filter_all_by_threshold(conn):
    """
    Filter through all products and return those under threshold & current inventory
    """
    curs = dbi.dict_cursor(conn)
    sql = """SELECT sku, title, max(timestamp) as latesttime, sum(amount) as inventory, threshold 
    FROM transaction INNER JOIN product USING (sku) GROUP BY sku HAVING inventory < threshold
    """
    curs.execute(sql)
    results = curs.fetchall()
    return results

def change_threshold(conn, sku, threshold):
    """
    Change the warning threshold of a product in the timeinv_db database
    """
    curs = dbi.dict_cursor(conn)
    sql = """update product 
    set threshold = %s 
    where sku = %s"""
    curs.execute(sql, [threshold, sku])
    conn.commit()

def record_sale(conn, sku, amount, timestamp, last_modified_by):
    """
    Record a sale in transaction table in the timeinv_db database
    """
    curs = dbi.dict_cursor(conn)
    sql = """insert into transaction
    (timestamp, sku, amount, last_modified_by) values (%s, %s, %s, %s)"""
    curs.execute(sql, [timestamp, sku, amount, last_modified_by])
    conn.commit()

def get_all_transactions(conn):
    curs = dbi.dict_cursor(conn)
    sql = "select tid, sku, title, timestamp, amount from product inner join transaction using (sku) order by timestamp DESC"
    curs.execute(sql)
    results = curs.fetchall()
    return results

def transaction_sort(conn, by, order):
    curs = dbi.dict_cursor(conn)
    # Prepared queries can only be used for values, not column names or order
    sql = "select transaction.tid, transaction.sku, product.title, transaction.timestamp, transaction.amount from product, transaction where product.sku = transaction.sku order by " + by +  " " + order
    curs.execute(sql)
    results = curs.fetchall()
    return results

def transaction_search(conn, search_type, query):
    """
    Returns a list of all products that contain the query string
    """
    curs = dbi.dict_cursor(conn)
    sql = """select tid, sku, title, timestamp, amount FROM product INNER JOIN transaction USING (sku) where """ + search_type + """ like %s """
    curs.execute(sql, ['%' + query + '%'])
    results = curs.fetchall()
    return results
