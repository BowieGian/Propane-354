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


def create_table(connection, sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
    except Error as e:
        print(e)

        
def main():
    database = 'propane354.db'

    sql_create_employee = '''
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

    sql_create_employee_qualification = '''
        CREATE TABLE IF NOT EXISTS employee_qualification(
            employee_id integer,
            qualification text,
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
    connection = create_connection(database)
    
    if (connection):
        # create tables
        create_table(connection, sql_create_employee)
        create_table(connection, sql_create_employee_qualification)
    else:
        print('Failed to create database connection.')


if __name__ == '__main__':
    main()


