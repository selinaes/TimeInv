# =================================================================================
#  TimeInv, an Inventory Management App for CS304 Project Spring '22 
#  Authors: Francisca Moya Jimenez, Jiawei Liu, Candice Ye, and Diana Hernandez
# =================================================================================

from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, jsonify, abort)
app = Flask(__name__)

import sys, os, random, datetime
import user, dashboard, products as prod, transaction, orders, access, exceptions
import cs304dbi as dbi
from pymysql import IntegrityError, MySQLError
import bcrypt

# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
# Image upload
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
        row = user.get_password_by_username(conn, username)
        if row is None:
            flash("Login incorrect. No account for the given username.", "error")
            return render_template('login.html')
        
        stored = row['hashed']
        hashed2 = bcrypt.hashpw(passwd1.encode('utf-8'),
                            stored.encode('utf-8'))
        hashed2_str = hashed2.decode('utf-8')

        if hashed2_str == row['hashed']:
            session['username'] = username
            session['logged_in'] = True
            permissions = user.get_permissions(conn, username)
            session['permissions'] = permissions.get('permission')
            return redirect(url_for('index'))

        flash("Login incorrect. Wrong password.", "error")
        return render_template('login.html')

@app.route('/signup/', methods = ['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    
    # Request is POST
    else:
        # Sign up
        username = request.form.get('username')
        passwd = request.form.get('password')
        hashed = bcrypt.hashpw(passwd.encode('utf-8'),
                           bcrypt.gensalt())
        stored = hashed.decode('utf-8')
        conn = dbi.connect()

        try:
            user.insert_new_account(conn, username, stored)
            flash("The account was successfully created.", "success")
            user.set_login_info(conn, username)
            return redirect(url_for('index'))

        # Username is longer than 10 characters or user doesn't exist
        # in the organization
        except (exceptions.UsernameFormatError, exceptions.UsernameNonExistent) as e:
            flash(e.message, 'error')
            return render_template('signup.html')

        # Username is taken
        except IntegrityError:
            flash("The username you chose is taken. Please choose another username.", "error")
            return render_template('signup.html')

        # Any other error that might arise
        except Exception as e:
            flash("There was an error creating the account. Please try again.", "error")
            return render_template('signup.html')


@app.route('/logout/', methods = ['GET', 'POST'])
def logout():
    if ('username' in session and 'logged_in' in session):
        session.pop('username')
        session.pop('logged_in')
    return redirect(url_for('index'))

@app.route('/', methods = ['GET','POST'])
def index():
    permissions = session.get('permissions', '')
    username = session.get('username', '')

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
        return render_template('main.html', results = results, permissions = permissions, username = username)
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
                flash("Sale was successfully registered", "success")

        # Catch errors:
        # Product with the given SKU doesn't exist 
        # If product availability is low when performing a sale
        except (exceptions.ProductNonExistent, exceptions.LowInventory) as e:
            flash(e.message, 'error')

        # Catch any other unexpected exceptions
        except Exception:
            flash("Error processing form. Try again.", "error")

        return render_template('main.html', permissions = permissions, username = username)

@app.route('/products/', methods = ['GET', 'POST'])
def products():
    # Check permission levels
    permissions = session.get('permissions', '')
    username = session.get('username', '')

    if not access.has_permissions('product'):
        flash("You attempted to access a forbidden page. Please log in again.", "error")
        return redirect(url_for('login'))

    conn = dbi.connect()
    if request.method == 'GET':
        if request.args:
            if request.args.get('search') or request.args.get('search') == '':
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
        open_new_product = 'False', 
        permissions = permissions, username = username)

    # Request is POST. Add a new product.
    else:
        product_data = {'name': request.form.get('product-name', ''),
        'sku': request.form.get('product-sku', ''), 
        'price': request.form.get('product-price', '')}
        try:
            # Handle picture
            file = request.files.get('picture')
            
            try: 
                file_name = prod.upload_file(file, ALLOWED_EXTENSIONS, product_data['sku'], 
                app.config['UPLOADS'])

            # Exception if product has incorrect format
            except exceptions.FileHasIncorrectFormat as e:
                flash(e.message, "error")
                results = prod.get_all_products(conn)
                return render_template('products.html', products=results, product_data=product_data, 
                permissions=permissions, username = username)

            # Any other unexpected exceptions
            except Exception as e: # Early return and flash if there are any issues uploading a picture
                flash("Error adding the product. The picture added could not be uploaded.", "error")
                results = prod.get_all_products(conn)
                return render_template('products.html', products=results, product_data=product_data, 
                permissions=permissions, username = username)
            
            
            # If file upload was sucessful, insert the product 
            prod.product_insert(conn, product_data['sku'], product_data['name'], 
            product_data['price'], session.get('username'), file_name)
            results = prod.get_all_products(conn)
            flash("The product was successfully added", "success")
            return render_template('products.html', products=results, product_data={},
             permissions = permissions, username = username)

        # SKU of product added already corresponds to another product
        except IntegrityError as e:
            print(e)
            flash('Error adding the product. The SKU indicated already corresponds to another product.'
                , "error")
            results = prod.get_all_products(conn)
            return render_template('products.html', products=results, product_data={}, 
            permissions=permissions, username = username)


        # Catch any other unexpected error
        except Exception as e:
            flash('Error adding the product. Please try again.', "error")
            results = prod.get_all_products(conn)
            return render_template('products.html', products=results, product_data={}, 
            permissions=permissions, username = username)


@app.route('/products/edit/<sku>', methods=['GET', 'POST'])
def edit_product(sku):
    permissions = session.get('permissions', '')
    username = session.get('username', '')

    # Check permission levels
    permissions = session.get('permissions', '')
    if not access.has_permissions('product'):
        flash("You attempted to access a forbidden page. Please log in again.", "error")
        return redirect(url_for('login'))

    conn = dbi.connect()
    results = prod.get_all_products(conn)
    product_exists = prod.sku_exists(conn, sku)

    # If SKU doesn't exist, throw an error
    if not product_exists:
        return abort(404)

    # Request is GET
    if request.method == 'GET':
        return render_template('products.html', sku = sku, products=results, edit=True, 
        permissions=permissions, username = username)

    # Request is POST
    else:
        product_data = {'name': request.form.get('product-name', ''),
        'sku': request.form.get('product-sku', ''), 
        'price': request.form.get('product-price', '')}
        try:
            # Handle picture
            file = request.files.get('picture')
            try: 
                file_name = prod.upload_file(file, ALLOWED_EXTENSIONS, sku, 
                app.config['UPLOADS'])

            # Flash informative error message if file has incorrect format
            except exceptions.FileHasIncorrectFormat as e:
                flash(e.message, "error")
                results = prod.get_all_products(conn)
                return render_template('products.html', sku = sku, edit=True,
                products=results, permissions=permissions, username = username)

            # Catch all other possible errors
            except Exception:
                flash("Error editing the product. The picture added could not be uploaded.",
                     "error")
                results = prod.get_all_products(conn)
                return render_template('products.html', sku = sku, edit=True,
                products=results, permissions=permissions, username = username)
            
            # If no issues with picture, try to update product
            updated_products = prod.update_product(conn, request.form['product-name'], 
                            request.form['product-price'], session.get('username'), 
                            file_name, sku, request.form['product-sku'])

            flash("The product was sucessfully updated.", "success")

            # SKU hasn't changed
            if sku == request.form['product-sku']:
                return render_template('products.html', sku = sku, 
                        products=updated_products, edit=True, 
                        permissions = permissions, username = username)
            # SKU has changed, we need to redirect
            else:
                return redirect(url_for('edit_product', sku = request.form['product-sku']))

        # Flash informative message if the SKU provided already exists
        # IntegrityError wasn't catching this so I had to use a more generic type of error
        except MySQLError:
            flash("""Error updating the product. The SKU provided already identifies 
                    another product.""", "error")
            return render_template('products.html', sku = sku, 
            products=results, edit=True, permissions = permissions, username = username)
            
        # Catch any other unexpected error
        except Exception as e:
            print(e.args)
            flash("Error updating the product. Try again.", "error")
            return render_template('products.html', sku = sku, 
            products=results, edit=True, permissions = permissions, 
            username = username)
            

@app.route('/products/delete/<sku>', methods=['GET', 'POST'])
def delete_product(sku):

    # Check permission levels
    if not access.has_permissions('product'):
        flash("You attempted to access a forbidden page. Please log in again.", "error")
        return redirect(url_for('login'))

    if request.method == 'GET':
        redirect(url_for('products'))
        
    conn = dbi.connect()
    try:
        prod.delete_product_by_sku(conn, sku)
        flash("The product was sucessfully deleted.", "success")
        return redirect(url_for('products'))

    # Using generic error since I am not distinguishing between 
    # any specific errors in deleting when calling delete on MySQL
    except Exception as e:
        flash("Error. The product could not be deleted.", "error")
        return redirect(url_for('products'))

@app.route('/order_products/', methods = ['GET', 'POST'])
def order_products():
    
    # Check permission levels
    permissions = session.get('permissions', '')
    username = session.get('username', '')
    
    if not access.has_permissions('product'):
        flash("You attempted to access a forbidden page. Please log in again.", "error")
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('order.html', permissions = permissions, 
        username =  username)
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
            return render_template('order.html', permissions = permissions, 
            username =  username)

        # Flash informative message if product with SKU provided doesn't exist
        except IntegrityError:
            flash("""Error adding the order: the product with the SKU 
                provided doesn't exist.""","error")
            return render_template('order.html', permissions = permissions, 
            username = username)

        # Catching any other unexpected errors
        except Exception as e:
            flash("Error adding the order.", "error")
            return render_template('order.html', permissions = permissions, 
            username = username)

@app.route('/transactions/')
def transactions():
    
    # Check permission levels
    permissions = session.get('permissions', '')
    username = session.get('username', '')
    
    if not access.has_permissions('transactions'):
        flash("You attempted to access a forbidden page. Please log in again.", "error")
        return redirect(url_for('login'))

    conn = dbi.connect()
    if request.args:
        search_query = request.args.get('search', '')
        if request.args.get('search') or request.args.get('search') == '':
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
    search = request.args.get('search'), permissions = permissions, 
    username = username)

@app.route('/manage_access/')
def users():
    
    # Check permission levels
    permissions = session.get('permissions', '')
    username = session.get('username', '')
    
    if not access.has_permissions('staff'):
        flash("You attempted to access a forbidden page. Please log in again.", "error")
        return redirect(url_for('login'))
    
    # Send current user
    username = session.get('username', '')
 
    if request.method == 'GET':
        conn = dbi.connect()
        results = access.get_all_access(conn, username)
        return render_template('manage-access.html', users = results, 
        permissions = permissions, username = username)

# AJAX routes
@app.route('/username_exists/<username>')
def username_exists(username):
    conn = dbi.connect()
    return jsonify(user.username_exists(conn, username))

@app.route('/delete_member/<username>', methods = ['DELETE'])
def delete_member(username):
    conn = dbi.connect()
    try:
        access.remove_member(conn, username)
        return jsonify(True)
    except:
        message = jsonify(message='Error removing member')
        return make_response(message, 400)

@app.route('/edit_member/', methods = ['POST'])
def edit_member():
    conn = dbi.connect()
    username = request.form.get('username', '')
    name = request.form.get('name', '')
    role = request.form.get('role', '')
    permission = request.form.get('permission', '')
    # Checking permission format
    if ',' in permission:
        permission_levels = permission.split(',')
        known_levels = 'product, transaction, staff, supplier, supplierTerm'
        if not all(element in known_levels for element in permission_levels):
           message = jsonify(message='Error editing member')
           return make_response(message, 400) 
    else:
        message = jsonify(message='Error editing member')
        return make_response(message, 400)
    try:
        result = access.edit_member(conn, username, name, role, permission)
        return jsonify(result)
    except:
        message = jsonify(message='Error editing member')
        return make_response(message, 400)

@app.route('/add_member/', methods = ['POST'])
def add_member():
    conn = dbi.connect()

    # Data
    username = request.form.get('username', '')
    name = request.form.get('name', '')
    role = request.form.get('role', '')
    permission = request.form.get('permission', '')

    # Checking permission format
    if ',' in permission:
        permission_levels = permission.split(',')
        known_levels = 'product, transaction, staff, supplier, supplierTerm'
        if all(element in known_levels for element in permission_levels) == False:
           message = jsonify(message='Error adding member')
           return make_response(message, 400) 
    else:
        message = jsonify(message='Error adding member')
        return make_response(message, 400)
    try:
        result = access.add_member(conn, username, name, role, permission)
        return jsonify(result)

    # Error if member is duplicated
    except IntegrityError:
        message = jsonify(message="""Error adding member. A member with the 
            username {} already exists.""".format(username))
        return make_response(message, 400)

    # Any other unexpected errors
    except Exception as e:
        message = jsonify(message='Error adding member')
        return make_response(message, 400)

@app.errorhandler(404)
def page_not_found(e):
    # Determine if user is logged in
    username = session.get('username') # None if user isn't logged in
    permissions = session.get('permissions', '')

    return render_template('error.html', username = username, 
    permissions = permissions), 404


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
