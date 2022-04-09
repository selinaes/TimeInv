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
    return render_template('main.html',title='Hello')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/products')
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
        return render_template('products.html', products = results, search = request.args.get('search'))

@app.route('/products/edit/<sku>', methods=['GET', 'POST'])
def edit_product(sku):
    conn = dbi.connect()
    results = utils.get_all_products(conn)
    product_exists = utils.sku_exists(conn, sku)

    if not product_exists:
        return abort(404)

    if request.method == 'GET':
        return render_template('product-edit.html', sku = sku, products=results)
    else:
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
            results = product_search(conn, request.args.get('by'), request.args.get('search'))
        else:
            results = product_sort(conn, request.args.get('sort'), request.args.get('order'))
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
