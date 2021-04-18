import pandas as pd
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
        return 'success'
    except Error as e:
        # print(e)
        return str(e)

        
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
    return insert(connection, sql, values)

    
def insert_employee_qualification(connection, values):
    sql = '''
        INSERT INTO employee_qualification(
            employee_id,
            qualification
        )
        VALUES(?, ?);
    '''
    return insert(connection, sql, values)


def insert_employee_availability(connection, values):
    sql = '''
        INSERT INTO employee_availability(
            employee_id,
            availability
        )
        VALUES(?, ?);
    '''
    return insert(connection, sql, values)


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
    return insert(connection, sql, values)


def insert_customer_phone_number(connection, values):
    sql = ''' 
        INSERT INTO customer_phone_number(
            customer_email,
            phone_number
        )
        VALUES(?, ?)
    '''
    return insert(connection, sql, values)


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
    return insert(connection, sql, values)


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
    return insert(connection, sql, values)


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
    return insert(connection, sql, values)


def insert_work_order_employee(connection, values):
    sql = '''
        INSERT INTO work_order_employee(
            work_order_number,
            employee_id
        )
        VALUES(?, ?);
    '''
    return insert(connection, sql, values)


def insert_work_order_propane_tank(connection, values):
    sql = '''
        INSERT INTO work_order_propane_tank(
            work_order_number,
            propane_tank_serial_number
        )
        VALUES(?, ?);
    '''
    return insert(connection, sql, values)


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
    return insert(connection, sql, values)


def select_all(connection, table_name):
    sql = f'''
        SELECT *
        FROM {table_name};
    '''
    select_all_results = pd.read_sql(sql, connection)
    return select_all_results

    
def group_by_aggregate_propane_tank(connection, group_by_attribute):
    sql = f'''
        SELECT {group_by_attribute}, COUNT(*) AS `Count`
        FROM propane_tank
        GROUP BY {group_by_attribute};
    '''
    propane_tank_counts = pd.read_sql(sql, connection)
    return propane_tank_counts


def select_propane_tank(connection, group_by_attribute):
    if (group_by_attribute == 'all'):
        select_propane_tank_results = select_all(connection, 'propane_tank')
    else:
        select_propane_tank_results = group_by_aggregate_propane_tank(connection, group_by_attribute)
    return select_propane_tank_results


def update_propane_tank_last_visual_check_date(connection, serial_number_updated_last_visual_check_date):
    sql = f'''
        UPDATE propane_tank
        SET last_visual_check_date = "{serial_number_updated_last_visual_check_date[1]}"
        WHERE serial_number = {serial_number_updated_last_visual_check_date[0]};
    '''
    
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        return 'success'
    except Error as e:
        return str(e)


def delete_work_order(connection, work_order_number):
    sql = f'''
        DELETE FROM work_order
        WHERE order_number = {work_order_number};
    '''
    
    try:
        # enable foreign key support https://sqlite.org/foreignkeys.html
        connection.execute('PRAGMA foreign_keys = ON;') 
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        return 'success'
    except Error as e:
        return str(e)


def left_join_customer_on_work_order(connection):
    sql = '''
    SELECT
        order_number, 
        order_status,
        customer_email, 
        customer.honorific AS customer_honorific, 
        customer.first_name AS customer_first_name, 
        customer.last_name AS customer_last_name
    FROM work_order
    LEFT JOIN customer ON customer.email = work_order.customer_email;
    '''
    left_join_results = pd.read_sql(sql, connection)
    return left_join_results

    
    
    
    
