# =================================================================================
#  Helper functions for new order page in app.py
#  Authors: Francisca Moya Jimenez, Jiawei Liu, Candice Ye, and Diana Hernandez
# =================================================================================

import cs304dbi as dbi

def add_product_order(conn, sku, units, timestamp, user):
    """
    Adds a product order to the transactions log

    Parameters:
        conn: a connection object
        sku (int): sku of product that was ordered
        units (int): number of units that were ordered
        timestamp (string): time at which transaction was made
        user (string): username of staff member that is adding
        the product order

    Returns:
        None
    """
    curs = dbi.dict_cursor(conn)
    sql = """insert into transaction 
            (timestamp, tid, sku, amount, last_modified_by)
            values (%s, NULL, %s, %s, %s)
        """
    curs.execute(sql, [timestamp, sku, units, user])
    conn.commit()
