# =================================================================================
#  Helper functions for supplierTerm page in app.py
#  Authors: Francisca Moya Jimenez, Jiawei Liu, Candice Ye, and Diana Hernandez
# =================================================================================

import cs304dbi as dbi

def get_all_supplierTerms(conn):
    """
    Returns all supplier terms in the current db
    Parameters:
        conn: a connection object
    Returns:
        The sid, company_name sku, title, cost for each term
        in reversed time order
    """
    curs = dbi.dict_cursor(conn)
    sql = """select sid, company_name, sku, title, cost
            from product 
            inner join supplierTerm using (sku) 
            inner join supplier using (sid) 
            order by sid DESC"""
    curs.execute(sql)
    results = curs.fetchall()
    return results

def term_sort(conn, by, order):
    """
    Returns a list of all supplier terms sorted in ascending or descending order
    Parameters:
        conn: a connection object
        by (string): column to sort the supplier term by
        order (string): asc or desc for ascending or descending order
    Returns:
        A list of dictionaries, where each dictionary is a term object, 
        sorted in asc or desc order for the given column
    """
    curs = dbi.dict_cursor(conn)
    order_by = {"sid", "sku", "title"}
    by_criterion = {"asc", "desc"}

    # Check inputs
    if by not in order_by or order not in by_criterion:
        raise Exception("Order by criterion is not allowed")

    # We can use user input because we have already vetted it
    sql = """select supplier.sid, supplier.company_name, product.sku, product.title, supplierTerm.cost 
            from product, supplier, supplierTerm
            where supplierTerm.sid = supplier.sid and supplierTerm.sku = product.sku
            order by """ + by + " " + order
    curs.execute(sql)
    results = curs.fetchall()
    return results

def term_search(conn, search_type, query):
    """
    Returns a list of all supplier terms that contain the query string
    in the given search_type column

    Parameters:
        conn: a connection object
        search_type (string): column to compare the query to
        query (string): string to search in the search_type column

    Returns:
        A list of dictionaries that contain the query string
        in the search_type column, where each dictionary is a 
        term object.
    """
    curs = dbi.dict_cursor(conn)
    cols = {"company_name", "sku", "title"}
    if search_type not in cols:
        raise Exception("Search not allowed for the given column")
    
    # We can use user input because we have already vetted it
    sql = """select sid, company_name, sku, title, cost
            from product 
            inner join supplierTerm using (sku) 
            inner join supplier using (sid)
            where """ + search_type + """ like %s """
    curs.execute(sql, ['%' + query + '%'])
    results = curs.fetchall()
    return results
