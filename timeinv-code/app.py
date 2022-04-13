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
app.config['UPLOADS'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 1*1024*1024 # 1 MB

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/products', methods = ['GET', 'POST'])
def products():
    conn = dbi.connect()
    if request.method == 'GET':
        if request.args:
            if request.args.get('search'):
                results = utils.product_search(conn, request.args.get('by'), 
                request.args.get('search'))
            else:
                results = utils.product_sort(conn, request.args.get('sort'), 
                request.args.get('order'))
        else:
            results = utils.get_all_products(conn)
        return render_template('products.html', 
        products = results, 
        search = request.args.get('search'),
        open_new_product = 'False')

    # Request is POST. Add a new product.
    else:
        product_data = {'name': request.form['product-name'],
        'sku': request.form['product-sku'], 'price': request.form['product-price']}
        try:
            utils.product_insert(conn, product_data['sku'], product_data['name'], 
            product_data['price'], 'at1') # Hard-coding last_modified_by until 
            # login implemented
            results = utils.get_all_products(conn)
            flash("The product was successfully added", "success")
            return render_template('products.html', products=results, product_data={})
        except Exception as e:
            print(str(e.args[1])) # Temporary. Helpful for debugging
            if ('Duplicate entry' in e.args[1]):
                flash('Error. The SKU indicated already corresponds to another product.', "error")
            else:
                flash('Error adding the product. Please try again.', "error")
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
        return render_template('products.html', sku = sku, products=results, edit=True)

    # Request is POST
    else:
        # SKU is unchanged
        new_sku = request.form['product-sku']
        if new_sku == sku:
            try:
                utils.update_product(conn, request.form['product-name'], 
                request.form['product-price'], 'at1', sku)
                flash("The product was sucessfully updated.", "success")
                results = utils.get_all_products(conn)
                return render_template('products.html', sku = sku, 
                products=results, edit=True)
            except Exception as e:
                flash("Error updating the product. Try again.", "error")
                return render_template('products.html', sku = sku, 
                products=results, edit=True)

        # SKU changed
        else:
            try:
                # Hard-coding last_modified_by until login is implemented
                utils.update_product_new_sku(conn, request.form['product-name'], 
                request.form['product-price'], 'at1', sku, request.form['product-sku'])
                flash("The product was sucessfully updated.", "success")
                results = utils.get_all_products(conn)
                return render_template('product-edit.html', 
                sku = request.form['product-sku'], products=results)

            except Exception as e:
                if 'duplicate entry' in e.args[1]:
                    flash("""Error updating the product. The SKU provided already identifies 
                    another product.""", "error")
                else:
                    flash("Error updating the product. Try again")
                return render_template('products.html', sku = sku, products=results,
                 edit=True)
            

@app.route('/products/delete/<sku>', methods=['POST'])
def delete_product(sku):
    conn = dbi.connect()
    try:
        utils.delete_product_by_sku(conn, sku)
        flash("The product was sucessfully deleted.", "success")
        return redirect(url_for('products'))
    except Exception as e:
        print(e)
        flash("Error. The product could not be deleted.", "error")
        return ('Error')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@app.errorhandler(405)
def page_not_found_wrong_method(e):
    return render_template('error.html'), 405

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
