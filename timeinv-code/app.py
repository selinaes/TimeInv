# =================================================================================
#  TimeInv, an Inventory Management App for CS304 Project Spring '22 
#  Authors: Francisca Moya Jimenez, Jiawei Liu, Candice Ye, and Diana Hernandez
# =================================================================================

from crypt import methods
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, jsonify, abort)
app = Flask(__name__)

import sys, os, imghdr, random, datetime
import dashboard, orders, products as prod, transaction, users
import cs304dbi as dbi
import bcrypt

# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
# Image upload (in progress)
app.config['UPLOADS'] = './static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 1*1024*1024 # 1 MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        # Log in
        username = request.form.get('username')
        passwd1 = request.form.get('password')

        conn = dbi.connect()
        row = users.get_password_by_username(conn, username)
        if row is None:
        # Same response as wrong password
            flash("Login incorrect. No account for the given username.", "error")
            return render_template('login.html')
        
        stored = row['hashed']
        hashed2 = bcrypt.hashpw(passwd1.encode('utf-8'),
                            stored.encode('utf-8'))
        hashed2_str = hashed2.decode('utf-8')

        if hashed2_str == row['hashed']:
            session['username'] = username
            session['logged_in'] = True
            return redirect(url_for('index'))

        flash("Login incorrect. Wrong password.", "error")
        return render_template('login.html')

@app.route('/signup/', methods = ['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    
    # Request is post
    else:
        # Sign up
        username = request.form.get('username')
        passwd = request.form.get('password')
        hashed = bcrypt.hashpw(passwd.encode('utf-8'),
                           bcrypt.gensalt())
        stored = hashed.decode('utf-8')
        conn = dbi.connect()

        try:
            users.insert_new_account(conn, username, stored)
            flash("The account was successfully created.", "success")
            return redirect(url_for('login'))

        except Exception as e:
            print(e.args)
            if len(e.args) == 1 and 'characters' in e.args[0]:
                flash(e.args[0], "error")
            elif len(e.args) == 2 and "key 'PRIMARY'" in e.args[1]:
                flash("The username you chose is taken. Please choose another username.", "error")
            else:
                flash("There was an error creating the account. Please try again.", "error")
            return render_template('signup.html')


@app.route('/logout/', methods = ['POST'])
def logout():
    if ('username' in session and 'logged_in' in session):
        session.pop('username')
        session.pop('logged_in')
    return redirect(url_for('index'))

@app.route('/', methods = ['GET','POST'])
def index():
    # Check if user is logged in
    if session.get('logged_in') == None:
        return redirect(url_for('login'))

    conn = dbi.connect()
    # 'GET' is for filtering the threshold check
    if request.method == 'GET':
        results = []
        if "check-all" in request.args:
            results = dashboard.filter_all_by_threshold(conn)
        else: 
            # Search by SKU
            if request.args.get('using') == 'sku':
                results = dashboard.inventory_by_sku(conn,request.args.get('number'))
                if len(results) == 1 and results[0]['sku'] == None:
                    results = []
                    flash("No products found for the given SKU", "error")
            # Search by threshold
            elif request.args.get('using') == 'threshold':
                results = dashboard.inventory_below_threshold(conn,request.args.get('number'))
                if len(results) == 0:
                    flash("No products found for the given threshold", "error")
        return render_template('main.html', results = results)
    # 'POST' is for 1. Modify Threshold 2. recording new sales
    else:
        try:
            if "threshold-form" in request.form:
                threshold_data = {
                    'threshold': request.form['threshold'],
                    'sku': request.form['threshold-sku']}
                dashboard.change_threshold(conn, threshold_data['sku'], threshold_data['threshold'])
                flash("Threshold updated", "success")
            elif "sale-form" in request.form:
                sale_data = {
                    'amount': request.form['sale-quantity'],
                    'sku': request.form['sale-sku']}
                # add logged-in staff detail & pass it to record_sale
                dashboard.record_sale(conn, sale_data['sku'],
                 sale_data['amount'], datetime.datetime.now(), 
                 session.get('username'))
                flash("Sale was sucessfully registered", "success")
        except Exception as e:
            print(e.args)
            if len(e.args) == 1 and 'availability' in e.args[0]:
                flash(e.args[0], "error")
            elif len(e.args) == 1 and 'No product found' in e.args[0]:
                flash(e.args[0], "error")
            else:
                flash("Error processing form. Try again.", "error")
        return render_template('main.html')

@app.route('/products/', methods = ['GET', 'POST'])
def products():
    # Check if user is logged in
    if session.get('logged_in') == None:
        return redirect(url_for('login'))

    conn = dbi.connect()
    if request.method == 'GET':
        if request.args:
            if request.args.get('search'):
                results = prod.product_search(conn, request.args.get('by'), 
                request.args.get('search'))
            else:
                results = prod.product_sort(conn, request.args.get('sort'), 
                request.args.get('order'))
        else:
            results = prod.get_all_products(conn)
        return render_template('products.html', 
        products = results, 
        search = request.args.get('search'),
        open_new_product = 'False')

    # Request is POST. Add a new product.
    else:
        product_data = {'name': request.form['product-name'],
        'sku': request.form['product-sku'], 'price': request.form['product-price']}
        try:
            # Handle picture
            file = request.files.get('picture')
            
            try: 
                file_name = prod.upload_file(file, ALLOWED_EXTENSIONS, product_data['sku'], 
                app.config['UPLOADS'])

            except Exception as e: # Early return and flash if there are any issues uploading a picture
                if (len(e.args) == 1 and 'incorrect format' in e.args[0]):
                    flash(e.args[0], "error")
                else: # Error unrelated to format
                    flash("Error adding the product. The picture added could not be uploaded.", "error")
                results = prod.get_all_products(conn)
                return render_template('products.html', products=results, product_data={})
            
            # If file upload was sucessful, insert the product 
            prod.product_insert(conn, product_data['sku'], product_data['name'], 
            product_data['price'], session.get('username'), file_name)
            results = prod.get_all_products(conn)
            flash("The product was successfully added", "success")
            return render_template('products.html', products=results, product_data={})

        except Exception as e:
            if (len(e.args) > 1 and 'Duplicate entry' in e.args[1]):
                flash('Error. The SKU indicated already corresponds to another product.'
                , "error")
            else:
                flash('Error adding the product. Please try again.', "error")
            results = prod.get_all_products(conn)
            return render_template('products.html', products=results, product_data={})


@app.route('/products/edit/<sku>', methods=['GET', 'POST'])
def edit_product(sku):
    # Check if user is logged in
    if session.get('logged_in') == None:
        return redirect(url_for('login'))

    conn = dbi.connect()
    results = prod.get_all_products(conn)
    product_exists = prod.sku_exists(conn, sku)

    # If SKU doesn't exist, throw an error
    if not product_exists:
        return abort(404)

    # Request is GET
    if request.method == 'GET':
        return render_template('products.html', sku = sku, products=results, edit=True)

    # Request is POST
    else:
        try:
            # Handle picture
            file = request.files.get('picture')
            try: 
                file_name = prod.upload_file(file, ALLOWED_EXTENSIONS, sku, 
                app.config['UPLOADS'])

            except Exception as e: # Early return and flash if there are any issues uploading a picture
                if (len(e.args) == 1 and 'incorrect format' in e.args[0]):
                    flash(e.args[0], "error")
                else: # Error unrelated to format
                    flash("Error adding the product. The picture added could not be uploaded.", "error")
                results = prod.get_all_products(conn)
                return render_template('products.html', products=results, product_data={})
            
            # If no issues with picture, try to insert product
            updated_products = prod.update_product(conn, request.form['product-name'], 
            request.form['product-price'], session.get('username'), file_name, sku, request.form['product-sku'])

            flash("The product was sucessfully updated.", "success")

            # SKU hasn't changed
            if sku == request.form['product-sku']:
                return render_template('products.html', sku = sku, 
                        products=updated_products, edit=True)
            # SKU has changed, we need to redirect
            else:
                return redirect(url_for('edit_product', sku = request.form['product-sku']))

        except Exception as e:
            if len(e.args) >= 2 and 'duplicate entry' in e.args[1]: 
                flash("""Error updating the product. The SKU provided already identifies 
                    another product.""", "error")
            else:
                flash("Error updating the product. Try again.", "error")
            return render_template('products.html', sku = sku, 
            products=results, edit=True)
            

@app.route('/products/delete/<sku>', methods=['POST'])
def delete_product(sku):
    # Check if user is logged in
    if session.get('logged_in') == None:
        return redirect(url_for('login'))

    conn = dbi.connect()
    try:
        prod.delete_product_by_sku(conn, sku)
        flash("The product was sucessfully deleted.", "success")
        return redirect(url_for('products'))
    except Exception as e:
        flash("Error. The product could not be deleted.", "error")
        return redirect(url_for('products'))

@app.route('/order_products/', methods = ['GET', 'POST'])
def order_products():
    # Check if user is logged in
    if session.get('logged_in') == None:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('order.html')
    # Request is POST
    else:
        conn = dbi.connect()
        try:
            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            orders.add_product_order(conn, request.form['product-sku'], 
            request.form['product-units'], date, session.get('username'))
            flash("""The order for product with
             SKU """+ request.form['product-sku'] +" was sucessfully added.", 
             "success")
            return render_template('order.html')
        except Exception as e:
            if len(e.args)  == 2 and 'FOREIGN KEY (`sku`)' in e.args[1]:
                flash("Error adding the order: the product with the SKU provided doesn't exist.",
                 "error")
            else:
                flash("Error adding order.", "error")
            return render_template('order.html')

@app.route('/transactions/')
def transactions():
    # Check if user is logged in
    if session.get('logged_in') == None:
        return redirect(url_for('login'))

    conn = dbi.connect()
    if request.args:
        if request.args.get('search'):
            results = transaction.transaction_search(conn, 
            request.args.get('by'), 
            request.args.get('search'))
        else:
            results = transaction.transaction_sort(conn, 
            request.args.get('sort'), 
            request.args.get('order'))
    else:
        results = transaction.get_all_transactions(conn)
    return render_template('transactions.html', transactions = results, 
    search = request.args.get('search'))


# AJAX routes
@app.route('/username_exists/', methods = ['POST'])
def username_exists():
    conn = dbi.connect()
    username = request.form.get('username', '')
    return jsonify(users.username_exists(conn, username))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@app.before_first_request
def init_db():
    dbi.cache_cnf()
    db_to_use = 'timeinv_db' 
    dbi.use(db_to_use)
    print('will connect to {}'.format(db_to_use))

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
