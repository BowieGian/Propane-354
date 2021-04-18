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

@app.route('/work-order/create', methods=['GET', 'POST'])
def workOrderAdd():
    database = 'propane354.db'
    connection = create_connection(database)

    if request.method == 'POST':
        form = {}
        attributes = [
            'rush_status', 'customer', 'po_number', 'work_to_be_done', 'tank_size',
            'liquid_vapour', 'qf', 'form_factor'
        ]

        for attribute in attributes:
            user_input = request.form[attribute]
            if (user_input != ''):
                form[attribute] = user_input
            else:
                form[attribute] = None
        
        return_value = 'success'
        new_work_orders = tuple(form.values())
        return_value = insert_work_order(connection, new_work_orders)
        if (return_value != 'success'):
            return render_template('work-order-create.html', error=return_value)
        else:
            return redirect(url_for('workOrderList'))
    else:
        return render_template('work-order-create.html', error='')

@app.route('/work-order/delete', methods=['GET', 'POST'])
def workOrderDelete():
    database = 'propane354.db'
    connection = create_connection(database)
    cursor = connection.cursor()
    work_orders = cursor.execute('SELECT order_number FROM work_order').fetchall();

    if request.method == 'POST':
        order_number = request.form['order_number']

        # delete work order --------------------------

        return redirect(url_for('workOrderList'))
    else:
        return render_template('work-order-delete.html', work_orders=work_orders)

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
        form = {}
        attributes = [
            'email', 'first_name', 'last_name', 'honorific', 'start_date', 'salary', 'position'
        ]

        for attribute in attributes:
            user_input = request.form[attribute]
            if (user_input != ''):
                form[attribute] = user_input
            else:
                form[attribute] = None

        return_value = 'success'
        new_employee = tuple(form.values())
        return_value = insert_employee(connection, new_employee)
        if (return_value != 'success'):
            return render_template('employee-add.html', error=return_value)
        else:
            return redirect(url_for('employeeList'))
    else:
        return render_template('employee-add.html')

@app.route('/employee-qualification-add', methods=['GET', 'POST'])
def employeeQualificationAdd():
    database = 'propane354.db'
    connection = create_connection(database)
    cursor = connection.cursor()
    employees = cursor.execute('SELECT first_name, id FROM employee').fetchall();

    if request.method == 'POST':
        form = {}
        attributes = [
            'id', 'qualification'
        ]

        for attribute in attributes:
            user_input = request.form[attribute]
            if (user_input != ''):
                form[attribute] = user_input
            else:
                form[attribute] = None

        if id == "Select":
            return render_template('employee-qualification-add.html', employees=employees)

        return_value = 'success'
        new_employee_qualification = tuple(form.values())
        return_value = insert_employee_qualification(connection, new_employee_qualification)

        if (return_value != 'success'):
            return render_template('employee-qualification-add.html', employees=employees, error=return_value)
        else:
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
        form = {}
        attributes = [
            'vin', 'license_plate_number', 'capacity', 'passenger_limit'
        ]

        for attribute in attributes:
            user_input = request.form[attribute]
            if (user_input != ''):
                form[attribute] = user_input
            else:
                form[attribute] = None

        return_value = 'success'
        new_vehicle = tuple(form.values())
        return_value = insert_truck(connection, new_vehicle)

        if (return_value != 'success'):
            return render_template('vehicles-add.html', error=return_value)
        else:
            return redirect(url_for('vehicles'))
    else:
        return render_template('vehicles-add.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

if __name__ == "__main__":
    app.run(debug=True)
