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

def insert_customer(connection, values):
    sql = '''
        INSERT INTO customer(
            email,
            company,
            credit_limit,
            first_name,
            last_name,
            suffix,
            unit_number,
            street_number,
            suburb,
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

        # insert a customer into the `customer` table
        customer1 = ('JohnSmith@bigCompany.com', 'bigCompany', 2500, 'John', 'Smith', 'Sr.', 125, 25, 'Big St.', '555 555')  
        insert_customer(connection, customer1)
        customer2 = customer2 = ('WalterBiggins@smallCompany.com', 'smallCompany', 1500, 'Walter', 'Biggins', None, 493, 29, 'White Ave.', '934 135')  
        insert_customer(connection, customer2)

        # view tables - uncomment line in the insert function to commit changes
        employee = pd.read_sql('SELECT * FROM employee;', connection)
        employee_qualifications = pd.read_sql('SELECT * FROM employee_qualification', connection)
        customer = pd.read_sql('SELECT * FROM customer', connection)

        print('Employee:\n', employee, '\n', sep='')
        print('Employee Qualifications:\n', employee_qualifications, sep='')
        print('Customer:\n', customer, '\n', sep='')

    else:
        print("Failed to create database connection.")


if __name__ == '__main__':
    main()
        