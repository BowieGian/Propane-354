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


def insert_employee_availability(connection, values):
    sql = '''
        INSERT INTO employee_availability(
            employee_id,
            availability
        )
        VALUES(?, ?);
    '''
    insert(connection, sql, values)


def insert_work_order(connection, values):
    sql = '''
        INSERT INTO work_order(
            order_number,
            employee_id,
            customer_email,
            order_total,
            order_status,
            payment_method,
            rush_level,
            order_date,
            po_number,
            expected_completion_date
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?,);
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


def main():
    database = 'propane354.db'

    connection = create_connection(database)
    
    if (connection):
        # insert an employee into the `employee` table  
        employee1 = ('John', 'Doe', 'SomeSuffix', '2021-03-05', 42000, 'Laborer')
        insert_employee(connection, employee1)

        # insert a qualification into the `employee_qualification` table
        employee1_qualifications = (1, 'Certified Inspector')
        insert_employee_qualification(connection, employee1_qualifications)

        # view tables - uncomment line in the insert function to commit changes
        employee = pd.read_sql('SELECT * FROM employee;', connection)
        employee_qualifications = pd.read_sql('SELECT * FROM employee_qualification', connection)

        print('Employee:\n', employee, '\n', sep='')
        print('Employee Qualifications:\n', employee_qualifications, sep='')
    else:
        print("Failed to create database connection.")


if __name__ == '__main__':
    main()
        
