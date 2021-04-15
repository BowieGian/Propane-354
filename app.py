import pandas as pd
import sqlite3

from flask import Flask, render_template, url_for, request, redirect
from our_sql import *
from sqlite3 import Error

app = Flask(__name__)

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

@app.route('/inventory/update', methods=['GET', 'POST'])
def inventoryUpdate():
    database = 'propane354.db'
    connection = create_connection(database)
    cursor = connection.cursor()

    serial_numbers = cursor.execute('SELECT serial_number FROM propane_tank WHERE type_of_tank = "Fiber";').fetchall()
    fiber_serial_number_last_visual_check_date = pd.read_sql('SELECT serial_number, last_visual_check_date FROM propane_tank WHERE type_of_tank = "Fiber";', connection)    

    if request.method == 'POST':
        serial_number = request.form['serial_number']
        updated_last_visual_check_date = request.form['last_visual_check_date']

        serial_number_updated_last_visual_check_date = [serial_number, updated_last_visual_check_date]
        return_value = update_propane_tank_last_visual_check_date(connection, serial_number_updated_last_visual_check_date)
        if (return_value != 'success'):
            return render_template(
                'inventory-update.html',
                tables=[fiber_serial_number_last_visual_check_date.to_html(classes='data', index=False)],
                titles=fiber_serial_number_last_visual_check_date.columns.values,
                error=return_value,
                serial_numbers=serial_numbers
            ) 
        else:
            fiber_serial_number_last_visual_check_date = pd.read_sql('SELECT serial_number, last_visual_check_date FROM propane_tank WHERE type_of_tank = "Fiber";', connection)
            return render_template(
                'inventory-update.html',
                tables=[fiber_serial_number_last_visual_check_date.to_html(classes='data', index=False)],
                titles=fiber_serial_number_last_visual_check_date.columns.values,
                error='',
                serial_numbers=serial_numbers
            ) 
    else:
        return render_template(
            'inventory-update.html',
            tables=[fiber_serial_number_last_visual_check_date.to_html(classes='data', index=False)],
            titles=fiber_serial_number_last_visual_check_date.columns.values,
            error='',
            serial_numbers=serial_numbers
        )
    
@app.route('/inventory/add', methods=['GET', 'POST'])
def inventoryAdd():
    database = 'propane354.db'
    connection = create_connection(database)
    cursor = connection.cursor()

    retail_employees = cursor.execute('SELECT id FROM employee WHERE position = "Retail";').fetchall();
    customer_emails = cursor.execute('SELECT email FROM customer;').fetchall();
    
    if request.method == 'POST':
        form = {}
        attributes = [
            'serial_number', 'manufacturer', 'expiration_date', 'quick_fill', 'form_factor',
            'tare_weight', 'water_capacity', 'liquid_vapor', 'rust_level', 'production_date',
            'last_visual_check_date', 'type_of_tank', 'sold_by_employee_id',
            'sold_to_customer_email', 'sell_date'
        ]

        for attribute in attributes:
            user_input = request.form[attribute]
            if (user_input != ''):
                form[attribute] = user_input
            else:
                form[attribute] = None

        return_value = 'success'
        new_propane_tank_values = tuple(form.values())
        return_value = insert_propane_tank(connection, new_propane_tank_values)
        if (return_value != 'success'):
            return render_template('inventory-add.html', retail_employees=retail_employees, customer_emails=customer_emails, error=return_value)
        else:
            return render_template('inventory-add.html', retail_employees=retail_employees, customer_emails=customer_emails, error='')
    else:
        return render_template('inventory-add.html', retail_employees=retail_employees, customer_emails=customer_emails, error='')

@app.route('/inventory/list', methods=['GET', 'POST'])
def inventoryList():
    database = 'propane354.db'
    connection = create_connection(database)

    group_by_attribute = request.form['group-by']
    select_propane_tank_results = select_propane_tank(connection, group_by_attribute)    

    return render_template(
        'inventory-list.html',
        tables=[select_propane_tank_results.to_html(classes='data', index=False)],
        titles=select_propane_tank_results.columns.values
    )

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
    database = 'propane354.db'
    connection = create_connection(database)

    test_sql = f'''
        SELECT *
        FROM truck
    '''

    df = pd.read_sql(test_sql, connection)

    return render_template('vehicles.html', tables=[df.to_html(classes='data', index=False)], titles=df.columns.values)

@app.route('/vehicles/add', methods=['GET', 'POST'])
def vehiclesAdd():
    database = 'propane354.db'
    connection = create_connection(database)

    if request.method == 'POST':
        vin = request.form['vin']
        license_plate_number = request.form['license_plate_number']
        capacity = request.form['capacity']
        passenger_limit = request.form['passenger_limit']

        insert_truck(connection, (vin, license_plate_number, capacity, passenger_limit))

        return redirect(url_for('vehicles'))
    else:
        return render_template('vehicles-add.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

if __name__ == "__main__":
    app.run(debug=True)
