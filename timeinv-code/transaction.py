# =================================================================================
#  Helper functions for transaction page in app.py
#  Authors: Francisca Moya Jimenez, Jiawei Liu, Candice Ye, and Diana Hernandez
# =================================================================================

import cs304dbi as dbi
import exceptions

def get_all_transactions(conn):
    """
    Returns all transactions in the current db
    Parameters:
        conn: a connection object
    Returns:
        The tid, sku, title, timestamp, and amount for each transaction
        in reversed time order
    """
    curs = dbi.dict_cursor(conn)
    sql = """select tid, sku, title, timestamp, amount, transaction.last_modified_by as responsible
            from product inner join transaction using (sku) order by timestamp DESC"""
    curs.execute(sql)
    results = curs.fetchall()
    return results

def transaction_sort(conn, by, order):
    """
    Returns a list of all transactions sorted in ascending or descending order
    Parameters:
        conn: a connection object
        by (string): column to sort the transactions by
        order (string): asc or desc for ascending or descending order
    Returns:
        A list of dictionaries, where each dictionary is a transaction object, 
        sorted in asc or desc order for the given column
    """
    curs = dbi.dict_cursor(conn)
    order_by = {"timestamp", "sku", "title"}
    by_criterion = {"asc", "desc"}

    # Check inputs
    if by not in order_by or order not in by_criterion:
        raise exceptions.TransactionSortInvalid()

    # We can use user input because we have already vetted it
    sql = """select transaction.tid, transaction.sku, product.title, 
            transaction.timestamp, transaction.amount, transaction.last_modified_by
            as responsible
            from product, transaction 
            where product.sku = transaction.sku 
            order by """ + by + " " + order
    curs.execute(sql)
    results = curs.fetchall()
    return results

def transaction_search(conn, search_type, query):
    """
    Returns a list of all transactions that contain the query string
    in the given search_type column

    Parameters:
        conn: a connection object
        search_type (string): column to compare the query to
        query (string): string to search in the search_type column

    Returns:
        A list of dictionaries that contain the query string
        in the search_type column, where each dictionary is a 
        transaction object.
    """
    curs = dbi.dict_cursor(conn)
    cols = {"timestamp", "sku", "title"}
    if search_type not in cols:
        raise exceptions.TransactionSearchInvalid()
    
    # We can use user input because we have already vetted it
    sql = """select tid, sku, title, timestamp, amount, transaction.last_modified_by
            as responsible
            FROM product INNER JOIN transaction USING (sku) 
            where """ + search_type + """ like %s """
    curs.execute(sql, ['%' + query + '%'])
    results = curs.fetchall()
    return results
