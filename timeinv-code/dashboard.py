# =================================================================================
#  Helper functions for dashboard page in app.py
#  Authors: Francisca Moya Jimenez, Jiawei Liu, Candice Ye, and Diana Hernandez
# =================================================================================

import cs304dbi as dbi
import exceptions


def inventory_below_threshold(conn, threshold):
    """
    Get all products below the given threshold

    Parameters:
        conn: a connection object
        threshold (int): the threshold below which a product need to be returned

    Returns:
        The sku, title, latest(transaction)time, current inventory, and threshold
        of products below the desired threshold
    """ 
    curs = dbi.dict_cursor(conn)
    sql = """select sku, title, max(timestamp) as latesttime, 
    sum(amount) as inventory, threshold 
    from transaction inner join product using (sku) 
    group by sku having inventory < %s
    """
    curs.execute(sql, [threshold])
    results = curs.fetchall()
    print(results)
    return results


def inventory_by_sku(conn, sku):
    """
    Get the requested sku product and its inventory information

    Parameters:
        conn: a connection object
        sku (int): the sku to be searched

    Returns:
        The sku, title, latest(transaction)time, current inventory, and threshold
        of the desired product
    """ 
    curs = dbi.dict_cursor(conn)
    sql = """SELECT sku, title, max(timestamp) as latesttime, 
    sum(amount) as inventory, threshold 
    FROM product INNER JOIN transaction 
    USING (sku) 
    WHERE sku = %s
    """
    curs.execute(sql, [sku])
    results = curs.fetchall()
    return results

def filter_all_by_threshold(conn):
    """
    Filter through all products and return those under threshold & current inventory

    Parameters:
        conn: a connection object

    Returns:
        The sku, title, latest(transaction)time, current inventory, and threshold
        of the products below their saved threshold
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

    Parameters:
        conn: a connection object
        sku: the sku of product to be changed
        threshold: the threshold to change to

    Returns:
        None
    """ 
    curs = dbi.dict_cursor(conn)
    # Add transaction to be able to update product despite of other
    # updates/deletions made to the product after select from another
    # thread. Rollback transaction if product doesn't exist.
    curs.execute("start transaction")
    sql1 = "select * from product where sku = %s"
    curs.execute(sql1, [sku])
    results = curs.fetchall()
    if len(results) == 0:
        curs.execute("rollback")
        raise exceptions.ProductNonExistent()
    sql2 = "update product set threshold = %s where sku = %s"
    curs.execute(sql2, [threshold, sku])
    curs.execute("commit")
    conn.commit()

def record_sale(conn, sku, amount, timestamp, last_modified_by):
    """
    Record a sale in transaction table in the timeinv_db database

    Parameters:
        conn: a connection object
        sku: the sku of product sold
        amount: the amount of product sold
        timestamp: the time when sale is recorded
        last_modified_by: the staff exercising the recording

    Returns:
        None
    """ 
    curs = dbi.dict_cursor(conn)
    sql1 = """select sum(amount) as inventory 
    from transaction group by sku having sku = %s
    """
    # Add transaction to show transaction inventory despite of other 
    # transactions happening in other threads.
    curs.execute("start transaction")
    curs.execute(sql1, [sku])
    result = curs.fetchall()
    if len(result) < 1:
        # Rollback (end) transaction if no product is found -- raise an error
        # that is picked up by the page and shown to the user
        curs.execute("rollback")
        raise exceptions.ProductNonExistent()
    else:
        if result[0]['inventory'] < int(amount):
        # Rollback (end) transaction if no product availability -- raise an error
        # that is picked up by the page and shown to the user
            curs.execute("rollback")
            raise exceptions.LowInventory(result[0]['inventory'])
    sql2 = """insert into transaction
    (timestamp, sku, amount, last_modified_by) values (%s, %s, %s, %s)"""
    curs.execute(sql2, [timestamp, sku, -int(amount), last_modified_by])
    curs.execute("commit")
    conn.commit()
