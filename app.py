import pandas as pd
import sqlite3

from flask import Flask, render_template, url_for, request, redirect
from our_sql import create_connection
from sqlite3 import Error

from datetime import date as dt
import datetime
import calendar as cd


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

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

@app.route('/inventory/add', methods=['GET', 'POST'])
def inventoryAdd():
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
def workOrderList():
    database = 'propane354.db'
    connection = create_connection(database)
    
    if (connection):
        cursor = connection.cursor()
    else:
        return "Failed to create database connection."

    test_sql = f'''
        SELECT *
        FROM work_order
    '''

    df = pd.read_sql(test_sql, connection)

    if request.method == 'POST':
        return render_template('work-order-list.html', tables=[df.to_html(classes='data', index=False)], titles=df.columns.values)
    else:
        return render_template('work-order-list.html', tables=[df.to_html(classes='data', index=False)], titles=df.columns.values)

    '''
    if request.method == 'POST':
        return 'Post'
    else:
        workOrders = cursor.execute('SELECT * FROM WorkOrder').fetchall()
        return render_template('work-order-list.html', workOrders=workOrders)
    '''

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
    today = dt.today()
    database = 'propane354.db'
    connection = create_connection(database)
    if (connection):
        cursor = connection.cursor()
    else:
        return "Failed to create database connection."
    
    query = "SELECT employee_id, availability FROM employee_availability"
    
    cursor.execute(query)
    
    data = list(cursor.fetchall()) 
    
    new_dict = {'todo' : [], 'date' : [],} 
    
    events = []
    
    f_wkday = datetime.datetime(today.year, today.month, 1)
    f_wkday = f_wkday.weekday()
    days_of_week=['Monday', 'Tuesday', 'Wednesday', 'Thursday','Friday','Saturday','Sunday']
    for x in data:
        
        wkday = days_of_week.index(x[1])

        cursor.execute ("SELECT first_name FROM employee WHERE id = {};".format(x[0]))
        name = str(cursor.fetchone())
        name = name[2:-3]
        
        if (f_wkday == wkday):
            i=1
        else:
            if wkday-f_wkday < 0:
                i = wkday - f_wkday + 7 + 1
            else:
                i = wkday - f_wkday + 1
        
        while i <= cd.monthrange(today.year, today.month)[1]:
            
            new_dict.update({'todo': name})
            new_dict.update({'date': str(today.year) + "-" + str(today.month).zfill(2) + "-" + str(i).zfill(2)})
            events.append(new_dict.copy())
            i+=7
    
    if request.method == 'POST':
        return 'Post'
    else:
        return render_template('calendar.html', events = events)

if __name__ == "__main__":
    app.run(debug=True)
