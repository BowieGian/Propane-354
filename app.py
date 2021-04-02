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
    connection = create_connection(database)

    if (connection):
        cursor = connection.cursor()
    else:
        return "Failed to create database connection."

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

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return 'Post'
    else:
        return render_template('home.html')

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if request.method == 'POST':
        return 'Post'
    else:
        return render_template('inventory.html')

@app.route('/inventory/list', methods=['GET', 'POST'])
def inventoryList():
    database = 'propane354.db'
    connection = create_connection(database)

    if (connection):
        cursor = connection.cursor()
    else:
        return "Failed to create database connection."

    group_by = request.form['group-by']

    test_sql = f'''
        SELECT {group_by}, COUNT(*) AS `Count`
        FROM propane_tank
        GROUP BY {group_by};
    '''
    
    item_counts = pd.read_sql(test_sql, connection)       

    if request.method == 'POST':
        return render_template('inventory-list.html', tables=[item_counts.to_html(classes='data')], titles=item_counts.columns.values)
    else:
        return render_template('inventory-list.html', tables=[item_counts.to_html(classes='data')], titles=item_counts.columns.values)

@app.route('/work-order', methods=['GET', 'POST'])
def workOrder():
    if request.method == 'POST':
        return 'Post'
    else:
        return render_template('work-order.html')

@app.route('/work-order/create', methods=['GET', 'POST'])
def workOrderCreate():
    if request.method == 'POST':
        return 'Post'
    else:
        return render_template('work-order-create.html')

@app.route('/work-order/list', methods=['GET', 'POST'])
def workOrderView():
    database = 'propane354.db'
    connection = create_connection(database)
    
    if (connection):
        cursor = connection.cursor()
    else:
        return "Failed to create database connection."

    if request.method == 'POST':
        return 'Post'
    else:
        workOrders = cursor.execute('SELECT * FROM WorkOrder').fetchall()
        return render_template('work-order-list.html', workOrders=workOrders)

@app.route('/employee-list', methods=['GET', 'POST'])
def employeeList():
    if request.method == 'POST':
        return 'Post'
    else:
        return render_template('employee-list.html')

@app.route('/customers', methods=['GET', 'POST'])
def customers():
    if request.method == 'POST':
        return 'Post'
    else:
        return render_template('customers.html')

@app.route('/vehicles', methods=['GET', 'POST'])
def vehicles():
    if request.method == 'POST':
        return 'Post'
    else:
        return render_template('vehicles.html')

@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    if request.method == 'POST':
        return 'Post'
    else:
        return render_template('calendar.html')

if __name__ == "__main__":
    app.run(debug=True)
