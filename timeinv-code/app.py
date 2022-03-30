from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)



import cs304dbi as dbi


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
    curs = dbi.dict_cursor(conn)
    if request.args:
        if request.args.get('search'):
            results = product_search(conn, request.args.get('by'), request.args.get('search'))
        else:
            results = product_sort(conn, request.args.get('sort'), request.args.get('order'))
    else:
        sql = "select * from product order by title"
        curs.execute(sql)
        results = curs.fetchall()
    return render_template('products.html', products = results)

def product_search(conn, search_type, query):
    curs = dbi.dict_cursor(conn)
    # Not using %s for search_type because cannot parametrize column names, only values
    sql = """select * from product 
    where """ + search_type + """ like %s order by title"""
    curs.execute(sql, ['%' + query + '%'])
    results = curs.fetchall()
    return results

def product_sort(conn, by, order):
    curs = dbi.dict_cursor(conn)
    # Prepared queries can only be used for values, not column names or order
    sql = "select * from product order by " + by +  " " + order
    curs.execute(sql)
    results = curs.fetchall()
    return results


@app.route('/products/<string:username>')
def products_addedby():
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    sql = """select * from product where 
    last_modified_by = %s"""
    curs.execute(sql, [username])
    results = curs.fetchall()
    return results

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

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
