# =================================================================================
#  Helper functions for the products page in app.py
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
    sql = "select * from product where " + search_type + " like %s order by title"
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
    sql = "select * from product where last_modified_by = %s"
    curs.execute(sql, [staff])
    results = curs.fetchall()
    return results

def product_insert(conn, sku, name, price, staff, image_name):
    """
    Inserts a new product into the database

    Parameters:
        conn: a connection object
        staff (string): the username of the staff 
        name (string): the name of the product to be inserted
        price (float): the price of the product to be inserted
        staff (string): the name of the staff posting the picture
        image_name (string): the name of the image uploaded for the product

    Returns:
        None
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
    sql = """select sku from product where sku = %s"""
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
        sql = """update product set sku = %s, title = %s, price = %s, 
                last_modified_by = %s, image_file_name = %s where sku = %s"""
        curs.execute(sql, [new_sku, title, price, last_modified_by, image, og_sku])
    
    else: # Image wasn't updated and we want to update the rest of the information
        sql = """update product set sku = %s, title = %s, price = %s, 
                last_modified_by = %s where sku = %s"""
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
