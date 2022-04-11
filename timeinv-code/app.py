from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify, abort)
from werkzeug.utils import secure_filename
app = Flask(__name__)

import cs304dbi as dbi
import utils 

import random

app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/products', methods = ['GET', 'POST'])
def products():
    conn = dbi.connect()
    if request.method == 'GET':
        if request.args:
            if request.args.get('search'):
                results = utils.product_search(conn, request.args.get('by'), request.args.get('search'))
            else:
                results = utils.product_sort(conn, request.args.get('sort'), request.args.get('order'))
        else:
            results = utils.get_all_products(conn)
        return render_template('products.html', 
        products = results, 
        search = request.args.get('search'),
        open_new_product = 'False')
    
    # Request is POST. Add a new product.
    else:
        product_exists = utils.sku_exists(conn, request.form['product-sku'])
        if product_exists:
            flash("""Error adding new product. 
            The SKU corresponds to an existing product.""", "error")
            results = utils.get_all_products(conn)
            product_data = {'name': request.form['product-name'],
             'sku': request.form['product-sku'], 'price': request.form['product-price']}
            return render_template('products.html', products=results, 
            open_new_product = 'True', product_data = product_data)
        else:
            try:
                curs = dbi.dict_cursor(conn)
                sql = """insert into product
                values (%s, %s, %s, %s, %s)"""
                curs.execute(sql, [request.form['product-sku'], 
                request.form['product-name'], 
                request.form['product-price'], 
                'at1', None]) # Hard-coding last_modified_by until login 
                conn.commit()
                flash("The product was sucessfully added.", "success")
                results = utils.get_all_products(conn)
                # Open empty modal when done.
                return render_template('products.html', products=results, product_data={})
            except:
                flash("There was an error adding the product. Try again.", "error")
                results = utils.get_all_products(conn)
                return render_template('products.html', products=results, product_data={})


@app.route('/products/edit/<sku>', methods=['GET', 'POST'])
def edit_product(sku):
    conn = dbi.connect()
    results = utils.get_all_products(conn)
    product_exists = utils.sku_exists(conn, sku)

    # If SKU doesn't exist, throw an error
    if not product_exists:
        return abort(404)

    # Request is GET
    if request.method == 'GET':
        return render_template('product-edit.html', sku = sku, products=results)

    # Request is POST
    else:
        # SKU is unchanged
        new_sku = request.form['product-sku']
        if new_sku == sku:
            try:
                curs = dbi.dict_cursor(conn)
                sql = """update product 
                set title = %s, price = %s, last_modified_by = %s
                where sku = %s"""
                curs.execute(sql, [request.form['product-name'], 
                request.form['product-price'], 
                'at1', sku])
                conn.commit()
                flash("The product was sucessfully updated.", "success")
                results = utils.get_all_products(conn)
                return render_template('product-edit.html', sku = sku, products=results)
            except:
                flash("Error updating the product. Try again.", "error")
                return render_template('product-edit.html', sku = sku, products=results)

        # SKU changed
        else:
            # Check if product sku is used in another product
            new_sku_exists = utils.sku_exists(conn, request.form['product-sku'])
            if new_sku_exists:
                flash("""Error updating the product. The SKU provided already identifies 
                another product.""", "error")
                return render_template('product-edit.html', sku = sku, products=results)
            
            # If new SKU doesn't already exist
            try:
                curs = dbi.dict_cursor(conn)
                sql = """update product 
                set sku = %s, title = %s, price = %s, last_modified_by = %s
                where sku = %s"""
                curs.execute(sql, [request.form['product-sku'], 
                request.form['product-name'], 
                request.form['product-price'], 
                'at1', sku])
                conn.commit()
                flash("The product was sucessfully updated.", "success")
                results = utils.get_all_products(conn)
                return render_template('product-edit.html', 
                sku = request.form['product-sku'], products=results)

            except:
                flash("Error updating the product. Try again.", "error")
                return render_template('product-edit.html', sku = sku, products=results)



@app.route('/products/<string:username>')
def products_addedby(username):
    conn = dbi.connect()
    results = utils.products_addedby(conn, username)
    return jsonify(results)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.before_first_request
def init_db():
    dbi.cache_cnf()
    db_to_use = 'timeinv_db' 
    dbi.use(db_to_use)
    print('will connect to {}'.format(db_to_use))

@app.route('/transactions')
def transactions():
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    if request.args:
        if request.args.get('search'):
            results = utils.product_search(conn, request.args.get('by'), request.args.get('search'))
        else:
            results = utils.product_sort(conn, request.args.get('sort'), request.args.get('order'))
    else:
        sql = "select sku, title, timestamp from product, transaction using (sku) order by timestamp, sku"
        curs.execute(sql)
        results = curs.fetchall()
    return render_template('transactions.html', transaction = results)

def transactions(conn, search_type, query):
    curs = dbi.dict_cursor(conn)
    # Not using %s for search_type because cannot parametrize column names, only values
    sql = """select product.sku, product.title, transacton.timestamp 
        from product, transaction
        using """ + search_type + """ like %s order by order by transaction.timestamp, product.sku"""
    curs.execute(sql, ['%' + query + '%'])
    results = curs.fetchall()
    return results

def transaction_sort(conn, by, order):
    curs = dbi.dict_cursor(conn)
    # Prepared queries can only be used for values, not column names or order
    sql = "select sku, title, timestamp from product, transaction using (sku) " + by +  " " + order
    curs.execute(sql)
    results = curs.fetchall()
    return results

if __name__ == '__main__':
    import sys, os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)
