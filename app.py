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

def insert(connection, sql, values):
    # adapted https://www.sqlitetutorial.net/sqlite-python/insert/
    
    try:
        cursor = connection.cursor()
        cursor.execute(sql, values)
        # insert an employee into the `employee` table  
        employee1 = ('John', 'Doe', 'SomeSuffix', '2021-03-05', 42000, 'Laborer')
        insert_employee(connection, employee1)
        employee2 = ('Bob', 'Smith', 'Mr.', '2021-01-05', 40000, 'Laborer')
        insert_employee(connection, employee2)

        # insert a qualification into the `employee_qualification` table
        employee1_qualifications = (1, 'Certified Inspector')
        insert_employee_qualification(connection, employee1_qualifications)
        employee2_qualifications = (2, 'Certified Inspector')
        insert_employee_qualification(connection, employee2_qualifications)

        # connection.commit() # uncomment to commit changes to database
    except Error as e:
        print(e)

def insert_employee(connection, values):
    sql = '''
        INSERT INTO employee(
            first_name, 
            last_name, 
            suffix, 
            start_date, 
            salary, 
            position
        )
        VALUES(?, ?, ?, ?, ?, ?);
    '''
    insert(connection, sql, values)

    
def insert_employee_qualification(connection, values):
    sql = '''
        INSERT INTO employee_qualification(
            employee_id,
            qualification
        )
        VALUES(?, ?);
    '''
    insert(connection, sql, values)

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
    if request.method == 'POST':
        return 'Post'
    else:
        return render_template('inventory-list.html')

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
