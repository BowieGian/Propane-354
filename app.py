import pandas as pd
import sqlite3

from flask import Flask, render_template, url_for, request, redirect
from our_sql import *
from sqlite3 import Error

from datetime import date as dt
import datetime
import calendar as cd


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
   

@app.route('/work-order/list')
def workOrderList():
    database = 'propane354.db'
    connection = create_connection(database)

    active_work_orders = pd.read_sql("""SELECT COUNT(*) AS IN_PROGRESS FROM work_order WHERE order_status LIKE 
    '%In Progress%'""", connection)
    onHold_work_orders = pd.read_sql("""SELECT COUNT(*) AS ON_HOLD FROM work_order WHERE order_status LIKE 
    '%On Hold%'""", connection)
    completed_work_orders = pd.read_sql("""SELECT COUNT(*) AS COMPLETED FROM work_order WHERE order_status LIKE 
    '%Complete%'""", connection)
    work_orders = pd.read_sql('SELECT * FROM work_order', connection)
    return render_template(
        'work-order-list.html', 
        tables=[
            active_work_orders.to_html(classes='data', index=False),
            onHold_work_orders.to_html(classes='data', index=False),
            completed_work_orders.to_html(classes='data', index=False),
            work_orders.to_html(classes='data', index=False)
            ], 
            titles=[active_work_orders.columns.values, onHold_work_orders.columns.values, 
            completed_work_orders.columns.values, work_orders.columns.values]
    )

@app.route('/work-order/create', methods=['GET', 'POST'])
def workOrderAdd():
    database = 'propane354.db'
    connection = create_connection(database)
    cursor = connection.cursor()

    customer_emails = cursor.execute('SELECT email FROM customer;').fetchall();

    if request.method == 'POST':
        form = {}
        attributes = [
            'rush_status', 'customer_email', 'po_number', 'work_to_be_done', 'tank_size',
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
            return render_template('work-order-create.html', customer_emails=customer_emails, error=return_value)
        else:
            return render_template('work-order-create.html', customer_emails=customer_emails, error='')
    else:
        return render_template('work-order-create.html', customer_emails=customer_emails, error='')

@app.route('/work-order/delete', methods=['GET', 'POST'])
def workOrderDelete():
    database = 'propane354.db'
    connection = create_connection(database)
    cursor = connection.cursor()
    work_order_numbers = cursor.execute('SELECT order_number FROM work_order').fetchall()

    work_orders = pd.read_sql('SELECT * FROM work_order;', connection)
    work_order_employee = pd.read_sql('SELECT * FROM work_order_employee;', connection)
    work_order_propane_tank = pd.read_sql('SELECT * FROM work_order_propane_tank;', connection)
    
    if request.method == 'POST':
        order_number = request.form['order_number']
        delete_work_order(connection, order_number)

        work_orders = pd.read_sql('SELECT * FROM work_order;', connection)
        work_order_employee = pd.read_sql('SELECT * FROM work_order_employee;', connection)
        work_order_propane_tank = pd.read_sql('SELECT * FROM work_order_propane_tank;', connection)
        return render_template(
            'work-order-delete.html',
            work_order_numbers=work_order_numbers,
            tables=[
                work_orders.to_html(classes='data', index=False),
                work_order_employee.to_html(classes='data', index=False),
                work_order_propane_tank.to_html(classes='data', index=False)
            ],
            titles=[work_orders.columns.values, work_order_employee.columns.values, work_order_propane_tank.columns.values]
        )
    else:
        return render_template(
            'work-order-delete.html',
            work_order_numbers=work_order_numbers,
            tables=[
                work_orders.to_html(classes='data', index=False),
                work_order_employee.to_html(classes='data', index=False),
                work_order_propane_tank.to_html(classes='data', index=False)
            ],
            titles=[work_orders.columns.values, work_order_employee.columns.values, work_order_propane_tank.columns.values]
        )

@app.route('/work-order/customer-name')
def workOrderJoin():
    database = 'propane354.db'
    connection = create_connection(database)
    
    df = left_join_customer_on_work_order(connection)
    return render_template('work-order-customer-name.html', tables=[df.to_html(classes='data', index=False)], titles=df.columns.values)

@app.route('/employee-list', methods=['GET', 'POST'])
def employeeList():
    database = 'propane354.db'
    connection = create_connection(database)
    test_sql = f'''
            SELECT *
            FROM employee
        '''

    filter = "all"

    if request.method == 'POST':
        filter = request.form['filter']

        if filter == "all":
            test_sql = f'''
                SELECT *
                FROM employee
            '''
        elif filter == "tank":
            test_sql = f'''
                SELECT *
                FROM employee E
                WHERE NOT EXISTS
                   (SELECT serial_number
                    FROM propane_tank
                    WHERE serial_number NOT IN
                       (SELECT serial_number
                        FROM delivery D
                        WHERE D.employee_id = E.id))
            '''
        elif filter == "truck":
            test_sql = f'''
                SELECT *
                FROM employee E
                WHERE NOT EXISTS
                   (SELECT vin
                    FROM truck
                    WHERE vin NOT IN
                       (SELECT vin
                        FROM delivery D
                        WHERE D.employee_id = E.id))
            '''
    df = pd.read_sql(test_sql, connection)

    return render_template('employee-list.html', tables=[df.to_html(classes='data', index=False)], titles=df.columns.values, filter=filter)

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
    database = 'propane354.db'
    connection = create_connection(database)

    test_sql = f'''
        SELECT *
        FROM customer
    '''

    df = pd.read_sql(test_sql, connection)
    return render_template('customers.html', tables=[df.to_html(classes='data', index=False)], titles=df.columns.values)

@app.route('/customers/add', methods=['GET', 'POST'])
def customersAdd():
    database = 'propane354.db'
    connection = create_connection(database)

    if request.method == 'POST':
        form = {}
        attributes = [
            'email', 'company', 'credit_limit', 'first_name', 'last_name', 'honorific', 
            'unit_number', 'street_number', 'street_name', 'postal_code'
        ]

        for attribute in attributes:
            user_input = request.form[attribute]
            if (user_input != ''):
                form[attribute] = user_input
            else:
                form[attribute] = None

        return_value = 'success'
        new_customer_values = tuple(form.values())
        return_value = insert_customer(connection, new_customer_values)
        
        if (return_value != 'success'):
            return render_template('customers-add.html', error=return_value)
        else:
            return redirect(url_for('customers'))
    else:
        return render_template('customers-add.html')


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
