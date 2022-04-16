from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify, abort)
from werkzeug.utils import secure_filename
app = Flask(__name__)

import cs304dbi as dbi
import utils 

import random
import datetime

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

@app.route('/', methods = ['GET','POST'])
def index():
    conn = dbi.connect()
    results = [{'sku': 'tbd', 'title': "Product's Name", 'latesttime': 'datetime', 'inventory': '0'}]
    # 'GET' is for filtering for threshold check
    if request.method == 'GET':
        if request.args.get('using') == 'sku':
            results = utils.inventory_by_sku(conn,request.args.get('number'))
        elif request.args.get('using') == 'threshold':
            results = utils.inventory_below_threshold(conn,request.args.get('number'))
    # 'POST' is for 1.Modify Threshold 2.recording new sales
    else:
        try:
            if "threshold-form" in request.form:
                threshold_data = {
                    'threshold': request.form['threshold'],
                    'sku': request.form['threshold-sku']}
                utils.change_threshold(conn, threshold_data['sku'], threshold_data['threshold'])
            elif "sale-form" in request.form:
                sale_data = {
                    'amount': request.form['sale-quantity'],
                    'sku': request.form['sale-sku']}
                # add logged-in staff detail & pass it to record_sale
                utils.record_sale(conn, sale_data['sku'], sale_data['amount'], datetime.datetime.now(), 'ad1')
        except Exception as e:
            flash("Error processing form. Try again.", "error")
    return render_template('main.html',results = results)

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

@app.before_first_request
def init_db():
    dbi.cache_cnf()
    db_to_use = 'timeinv_db' 
    dbi.use(db_to_use)
    print('will connect to {}'.format(db_to_use))

@app.route('/transactions')
def transactions():
    conn = dbi.connect()
    if request.method == 'GET':
        if request.args:
            if request.args.get('search'):
                results = utils.transaction_search(conn, request.args.get('by'), request.args.get('search'))
            else:
                results = utils.transaction_sort(conn, request.args.get('sort'), request.args.get('order'))
        else:
            results = utils.get_all_transactions(conn)
        return render_template('transactions.html', transactions = results)

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
