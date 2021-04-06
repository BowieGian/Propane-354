import pandas as pd
import sqlite3

from flask import Flask, render_template, url_for, request, redirect
from our_sql import create_connection
from sqlite3 import Error

app = Flask(__name__)

def create_connection(db_file):
    # taken from https://www.sqlitetutorial.net/sqlite-python/create-tables/
    
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)

    return connection

@app.route('/', methods=['GET', 'POST'])
def index():
    database = 'propane354.db'
    cursor = create_connection(database).cursor()
    employees = cursor.execute('SELECT first_name FROM employee').fetchall();

    if request.method == 'POST':
        first_name = request.form['first_name']
        id = request.form['id']

        # find if login exists
        if cursor.execute('SELECT id FROM employee WHERE first_name = ? AND id = ?', (first_name, id,)).fetchone():
            return redirect(url_for('home'))
        else:
            return render_template('login.html', employees=employees, loginFailed=True)
    else:
        return render_template('login.html', employees=employees, loginFailed=False)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

@app.route('/inventory/add', methods=['GET', 'POST'])
def inventoryAdd():
    database = 'propane354.db'
    connection = create_connection(database)

    if request.method == 'POST':
        size = request.form['size']
        manufacturer = request.form['manufacturer']
        form = request.form['form']
        quick_fill = request.form['quick_fill']
        material = request.form['material']

        # add to database ----------------------

        redirect(url_for('inventory'))
    else:
        return render_template('inventory-add.html')

@app.route('/inventory/list', methods=['GET', 'POST'])
def inventoryList():
    database = 'propane354.db'
    connection = create_connection(database)

    group_by = request.form['group-by']

    test_sql = f'''
        SELECT {group_by}, COUNT(*) AS `Count`
        FROM propane_tank
        GROUP BY {group_by};
    '''
    
    item_counts = pd.read_sql(test_sql, connection)       

    if request.method == 'POST':
        return render_template('inventory-list.html', tables=[item_counts.to_html(classes='data', index=False)], titles=item_counts.columns.values)
    else:
        return render_template('inventory-list.html', tables=[item_counts.to_html(classes='data', index=False)], titles=item_counts.columns.values)

@app.route('/work-order')
def workOrder():
    return render_template('work-order.html')

@app.route('/work-order/create', methods=['GET', 'POST'])
def workOrderCreate():
    if request.method == 'POST':
        return 'Post'
    else:
        return render_template('work-order-create.html')

@app.route('/work-order/list')
def workOrderList():
    database = 'propane354.db'
    connection = create_connection(database)

    test_sql = f'''
        SELECT *
        FROM work_order
    '''

    df = pd.read_sql(test_sql, connection)

    return render_template('work-order-list.html', tables=[df.to_html(classes='data', index=False)], titles=df.columns.values)

@app.route('/employee-list')
def employeeList():
    database = 'propane354.db'
    connection = create_connection(database)

    test_sql = f'''
        SELECT *
        FROM employee
    '''

    df = pd.read_sql(test_sql, connection)

    return render_template('employee-list.html', tables=[df.to_html(classes='data', index=False)], titles=df.columns.values)

@app.route('/employee-list/add', methods=['GET', 'POST'])
def employeeAdd():
    database = 'propane354.db'
    connection = create_connection(database)

    if request.method == 'POST':
        honorific = request.form['honorific']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        start_date = request.form['start_date']
        department = request.form['department']
        salary = request.form['salary']

        # add employee ------------------

        return redirect(url_for('empolyeeList'))
    else:
        return render_template('employee-add.html')

@app.route('/employee-qualification-add', methods=['GET', 'POST'])
def employeeQualificationAdd():
    database = 'propane354.db'
    connection = create_connection(database)
    cursor = connection.cursor()
    employees = cursor.execute('SELECT first_name FROM employee').fetchall();

    if request.method == 'POST':
        first_name = request.form['first_name']
        qualification = request.form['qualification']

        # add qualification ----------------------

        return redirect(url_for('employeeList'))
    else:
        return render_template('employee-qualification-add.html', employees=employees)

@app.route('/customers')
def customers():
    return render_template('customers.html')

@app.route('/vehicles')
def vehicles():
    return render_template('vehicles.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

if __name__ == "__main__":
    app.run(debug=True)
