# =================================================================================
#  Helper functions for app.py
#  Authors: Francisca Moya Jimenez, Jiawei Liu, Candice Ye, and Diana Hernandez
# =================================================================================

import cs304dbi as dbi
import os
from werkzeug.utils import secure_filename


def get_all_products(conn):
    """
    Returns all products in the current db
    Parameters:
        conn: a connection object
    Returns:
        A list of dictionaries, where each dictionary represents
        a product
    """
    curs = dbi.dict_cursor(conn)
    sql = "select * from product order by title"
    curs.execute(sql)
    results = curs.fetchall()
    return results


def product_sort(conn, by, order):
    """
    Returns a list of all products sorted in ascending or descending order
    Parameters:
        conn: a connection object
        by (string): column to sort the products by
        order (string): asc or desc for ascending or descending order
    Returns:
        A list of dictionaries, where each dictionary is a product object, 
        sorted in asc or desc order for the given column
    """
    curs = dbi.dict_cursor(conn)
    # Checking inputs
    order_by = {"price", "title", "sku"}
    direction = {"asc", "desc"}
    if by not in order_by or order not in direction:
        raise Exception("Type to sort by in products is not permitted")
    
    # We have already vetted the user input, so we can go ahead and use it
    sql = "select * from product order by " + by +  " " + order
    curs.execute(sql)
    results = curs.fetchall()
    return results


def product_search(conn, search_type, query):
    """
    Returns a list of all products that contain the query string
    in the given search_type column

    Parameters:
        conn: a connection object
        search_type (string): column to compare the query to
        query (string): string to search in the search_type column

    Returns:
        A list of dictionaries that contain the query string
        in the search_type column, where each dictionary is a 
        product object.
    """
    curs = dbi.dict_cursor(conn)
    order_by = {"price", "title", "sku"}
    if search_type not in order_by:
        raise Exception("Type to sort by in products is not permitted")
    
    # We can use search_type because we have already vetted the input
    sql = """select * from product 
    where """ + search_type + """ like %s order by title"""
    curs.execute(sql, ['%' + query + '%'])
    results = curs.fetchall()
    return results


def products_addedby(conn, staff):
    """
    Returns a list of all products that were added by a 
    specific staff member

    Parameters:
        conn: a connection object
        staff (string): the username of the staff 

    Returns:
        A list of dictionaries, where each dictionary is a 
        product object that was added by the given staff member.
    """
    curs = dbi.dict_cursor(conn)
    sql = """select * from product where 
    last_modified_by = %s"""
    curs.execute(sql, [staff])
    results = curs.fetchall()
    return results

def product_insert(conn, sku, name, price, staff, image_name):
    """
    Returns a list of all products that were added by a 
    specific staff member

    Parameters:
        conn: a connection object
        staff (string): the username of the staff 
        name (string): the name of the product to be inserted
        price (float): the price of the product to be inserted
        staff (string): the name of the staff posting the picture
        image_name (string): the name of the image uploaded for the product

    Returns:
        A list of dictionaries, where each dictionary is a 
        product object that was added by the given staff member.
    """
    curs = dbi.dict_cursor(conn)
    sql = """insert into product (sku, title, price, threshold, 
    last_modified_by, image_file_name)
    values (%s, %s, %s, %s, %s, %s)"""
    # Threshold starts as 0 by default
    curs.execute(sql, [sku, name, price, 0, 
    staff, image_name if image_name != '' else None]) 
    conn.commit()

def sku_exists(conn, sku):
    """
    Returns a boolean indicating whether a product
    with the given sku exists

    Parameters:
        conn: a connection object
        sku (int): product sku to be searched

    Returns:
        A boolean indicating whether a product
        with the given sku exists (True if it exists,
        False if it doesn't).
    """
    curs = dbi.dict_cursor(conn)
    sql = """select sku from product where 
    sku = %s"""
    curs.execute(sql, [sku])
    results = curs.fetchall()
    return len(results) > 0


def update_product(conn, title, price, last_modified_by, image, og_sku, new_sku):
    """
    Updates a product in the timeinv_db database with a new sku

    Parameters:
        conn: a connection object
        title (string): new product title
        price (float): new product price
        last_modified_by (string): username of staff that is
        updating the product
        og_sku (int): original product sku
        new_sku (int): new product sku

    Returns:
        A list of dictionary-type objects with the updated 
        product information
    """
    curs = dbi.dict_cursor(conn)
    if image != '': # Image was not added by the user
        sql = """update product 
        set sku = %s, title = %s, price = %s, last_modified_by = %s, image_file_name = %s
        where sku = %s"""
        curs.execute(sql, [new_sku, title, price, last_modified_by, image, og_sku])
    
    else: # Image wasn't updated and we want to update the rest of the information
        sql = """update product 
        set sku = %s, title = %s, price = %s, last_modified_by = %s
        where sku = %s"""
        curs.execute(sql, [new_sku, title, price, last_modified_by, og_sku])
    curs.execute("select * from product order by title")
    results = curs.fetchall()
    conn.commit()
    return results

def delete_product_by_sku(conn, sku):
    """
    Delets a product from the database with the given sku.

    Parameters:
        conn: a connection object
        sku (int): sku of product to be deleted

    Returns:
        None
    """
    curs = dbi.dict_cursor(conn)
    sql = "delete from product where sku = %s"
    curs.execute(sql, [sku])
    conn.commit()

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
    sql = """update product 
    set threshold = %s 
    where sku = %s"""
    curs.execute(sql, [threshold, sku])
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
    curs.execute("start transaction")
    curs.execute(sql1, [sku])
    result = curs.fetchall()
    if len(result) < 1:
        curs.execute("rollback")
        raise Exception("No product found with the SKU given")
    else:
        if result[0]['inventory'] < int(amount):
            curs.execute("rollback")
            raise Exception("""Not enough availability of the product to perform the sale.
            There are only """ + str(result[0]['inventory']) + " units available")
    sql2 = """insert into transaction
    (timestamp, sku, amount, last_modified_by) values (%s, %s, %s, %s)"""
    curs.execute(sql2, [timestamp, sku, -int(amount), last_modified_by])
    curs.execute("commit")
    conn.commit()

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
    sql = """select tid, sku, title, timestamp, amount 
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
        raise Exception("Order by criterion is not allowed")

    # We can use user input because we have already vetted it
    sql = """select transaction.tid, transaction.sku, product.title, 
    transaction.timestamp, transaction.amount 
    from product, transaction 
    where product.sku = transaction.sku 
    order by """ + order_by +  " " + order
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
        raise Exception("Search not allowed for the given column")
    
    # We can use user input because we have already vetted it
    sql = """select tid, sku, title, timestamp, amount 
    FROM product INNER JOIN transaction USING (sku) 
    where """ + search_type + """ like %s """
    curs.execute(sql, ['%' + query + '%'])
    results = curs.fetchall()
    return results

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


def upload_file(file, extension_list, sku, uploads):
    """
    Uploads a file to the files folder

    Parameters:
        file: file to be uploaded
        extension_list (list of strings): list with the 
            extensions that a user is allowed to upload
        sku (int): product sku for which to upload the picture to
        uploads: directory to which to upload the file

    Returns:
        A string with the file name that was uploaded
    """
    user_filename = file.filename
    filename = ''

    if user_filename != '': # User uploaded file
        ext = user_filename.split('.')[-1]
        if ext not in extension_list:
            raise Exception("Error inserting the product. File uploaded has incorrect format.")
        else:
            filename = secure_filename('{}.{}'.format(sku, ext))
            pathname = os.path.join(uploads, filename)
            file.save(pathname)

    return filename

def get_password_by_username(conn, username):
    """
    Returns the username and the hashed password for a given username.

    Parameters:
        conn: a connection object
        username (string): a username 

    Returns:
        None if the given username doesn't exist, and
        a dictionary-like object if the username exists
        with the username and the hashed password stored
    """
    curs = dbi.dict_cursor(conn)
    curs.execute("""SELECT username, hashed
                    FROM userpass
                    WHERE username = %s""",
                     [username])
    row = curs.fetchone()
    return row