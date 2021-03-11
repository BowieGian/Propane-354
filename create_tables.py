# functions and main adapted from
# https://www.sqlitetutorial.net/sqlite-python/create-tables/
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)

    return connection


def execute_sql(connection, sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
    except Error as e:
        print(e)


def create_tables(connection):
    create_table_sql = {}

    create_table_sql['employee'] = '''
        CREATE TABLE IF NOT EXISTS employee(
            id integer PRIMARY KEY AUTOINCREMENT,
            first_name text, 
            last_name text, 
            suffix text, 
            start_date text, 
            salary integer, 
            position text
        );
    '''

    create_table_sql['employee_qualification'] = '''
        CREATE TABLE IF NOT EXISTS employee_qualification(
            employee_id integer,
            qualification text,
            PRIMARY KEY (employee_id, qualification),
            FOREIGN KEY (employee_id) REFERENCES employee (id)
        );
    '''

    create_table_sql['employee_availability'] = '''
        CREATE TABLE IF NOT EXISTS employee_availability(
            employee_id integer,
            availability text,
            PRIMARY KEY (employee_id, availability),
            FOREIGN KEY (employee_id) REFERENCES employee (id)
        );
    '''

    sql_create_customer = '''
        CREATE TABLE IF NOT EXISTS customer(
            email text PRIMARY KEY,
            company text,
            credit_limit integer,
            first_name text,
            last_name text,
            suffix text,
            unit_number integer,
            street_number integer,
            suburb text,
            postal_code text
        );
    '''
    sql_create_customer_phone_number = '''
        CREATE TABLE IF NOT EXISTS customer_phone_number(
            customer_email text,
            phone_number integer,
            PRIMARY KEY (customer_email, phone_number),
            FOREIGN KEY (customer_email) REFERENCES customer (email)
        );
    '''

    sql_create_propane_tank = '''
        CREATE TABLE IF NOT EXISTS propane_tank(
            serial_number text PRIMARY KEY,
            expiration_date text,
            quick_fill text,
            form_factor text,
            tare_weight text,
            water_capacity text,
            DOT_TCStamp text,
            liquid_vapor text,
            rust_level text,
            production_date text,
            last_visual_check_date text,
            type_of_tank text,
            sold_by_employee_id int,
            sold_to_customer_email text,
            sell_date text,
            FOREIGN KEY (sold_by_employee_id) REFERENCES employee (id),
            FOREIGN KEY (sold_to_customer_email) REFERENCES customer (email)
        );
    '''

    sql_create_truck = '''
        CREATE TABLE IF NOT EXISTS truck(
            vin int PRIMARY KEY,
            license_plate_number text,
            capacity int,
            passenger_limit int
        )
    '''

    # connect to database
    create_table_sql['work_order'] = '''
        CREATE TABLE IF NOT EXISTS work_order(
            order_number integer,
            employee_id integer,
            customer_email text,
            order_total integer,
            order_status text,
            payment_method text,
            rush_level integer,
            order_date text;
            po_number integer,
            expected_completion_date text,
            PRIMARY KEY(
                order_number,
                employee_id,
                customer_email
            ),
            FOREIGN KEY (employee_id)
                REFERENCES employee (id),
            FOREIGN KEY(customer_email)
                REFERENCES customer (email) 
        );
    '''

    create_table_sql['work_order_propane_tank'] = '''
        CREATE TABLE IF NOT EXISTS work_order(
            work_order_number integer,
            propane_tank_serial_number integer,
            PRIMARY KEY(
                order_number,
                propane_tank_serial_number
            ),
            FOREIGN KEY (work_order_number)
                REFERENCES work_order (order_number),
            FOREIGN KEY(propane_tank_serial_number)
                REFERENCES propane_tank (serial_number) 
        );
    '''

    create_table_sql['delivery'] = '''
        CREATE TABLE IF NOT EXISTS delivery(
            employee_id integer,
            customer_email text,
            serial_number integer,
            vin text,
            delivery_date text,
            PRIMARY KEY (
                employee_id,
                customer_email,
                propane_tank_serial_number,
                vin
            ),
            FOREIGN KEY (employee_id)
                REFERENCES employee (id),
            FOREIGN KEY (customer_email)
                REFERENCES customer (email),
            FOREIGN KEY (propane_tank_serial_number)
                REFERENCES propane_tank (serial_number),
            FOREIGN KEY (vin)
                REFERENCES truck (vin)
        );
    '''

    for sql in create_table_sql.values():
        execute_sql(connection, sql)


def delete_tables(connection):
    # hard 
    tables = [
        'employee', 'employee_qualification', 'employee_availability',
        'work_order', 'work_order_propane_tank', 'delivery'
    ]

    delete_table_sql = [f'DROP TABLE IF EXISTS {table};' for table in tables]
    
    for sql in delete_table_sql:
        execute_sql(connection, sql)

        
def main():
    database = 'propane354.db'
    connection = create_connection(database)
    
    if (connection):
        create_tables(connection)
        # delete_tables(connection)
    else:
        print('Failed to create database connection.')


if __name__ == '__main__':
    main()


