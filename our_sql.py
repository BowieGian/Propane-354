import sqlite3
from sqlite3 import Error


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
        connection.commit() # uncomment to commit changes to database
    except Error as e:
        print(e)

        
def insert_employee(connection, values):
    sql = '''
        INSERT INTO employee(
            email,
            first_name, 
            last_name, 
            honorific, 
            start_date, 
            salary, 
            position
        )
        VALUES(?, ?, ?, ?, ?, ?, ?);
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


def insert_employee_availability(connection, values):
    sql = '''
        INSERT INTO employee_availability(
            employee_id,
            availability
        )
        VALUES(?, ?);
    '''
    insert(connection, sql, values)


def insert_customer(connection, values):
    sql = '''
        INSERT INTO customer(
            email,
            company,
            credit_limit,
            first_name,
            last_name,
            honorific,
            unit_number,
            street_number,
            street_name,
            postal_code
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    insert(connection, sql, values)


def insert_customer_phone_number(connection, values):
    sql = ''' 
        INSERT INTO customer_phone_number(
            customer_email,
            phone_number
        )
        VALUES(?, ?)
    '''
    insert(connection, sql, values)


def insert_propane_tank(connection, values):
    sql = '''
        INSERT INTO propane_tank(
            serial_number,
            manufacturer,
            expiration_date,
            quick_fill,
            form_factor,
            tare_weight,
            water_capacity,
            liquid_vapor,
            rust_level,
            production_date,
            last_visual_check_date,
            type_of_tank,
            sold_by_employee_id,
            sold_to_customer_email,
            sell_date
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    insert(connection, sql, values)


def insert_truck(connection, values):
    sql = ''' 
        INSERT INTO truck(
            vin,
            license_plate_number,
            capacity,
            passenger_limit
        )
        VALUES(?, ?, ?, ?)
    '''
    insert(connection, sql, values)


def insert_work_order(connection, values):
    sql = '''
        INSERT INTO work_order(
            order_number,
            customer_email,
            order_total,
            order_status,
            payment_method,
            rush_level,
            order_date,
            po_number,
            expected_completion_date
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''
    insert(connection, sql, values)


def insert_work_order_employee(connection, values):
    sql = '''
        INSERT INTO work_order_employee(
            work_order_number,
            employee_id
        )
        VALUES(?, ?);
    '''
    insert(connection, sql, values)


def insert_work_order_propane_tank(connection, values):
    sql = '''
        INSERT INTO work_order_propane_tank(
            work_order_number,
            propane_tank_serial_number
        )
        VALUES(?, ?);
    '''
    insert(connection, sql, values)


def insert_delivery(connection, values):
    sql = '''
        INSERT INTO delivery(
            employee_id,
            customer_email,
            serial_number,
            vin,
            delivery_date
        )
        VALUES(?, ?, ?, ?, ?);
    '''
    insert(connection, sql, values)
