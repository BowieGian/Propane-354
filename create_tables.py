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
            id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
            email text NOT NULL UNIQUE,
            first_name text NOT NULL, 
            last_name text NOT NULL, 
            suffix text NOT NULL, 
            start_date text NOT NULL, 
            salary integer NOT NULL, 
            position text NOT NULL
        );
    '''

    create_table_sql['employee_qualification'] = '''
        CREATE TABLE IF NOT EXISTS employee_qualification(
            employee_id integer NOT NULL,
            qualification text NOT NULL,
            PRIMARY KEY (employee_id, qualification),
            FOREIGN KEY (employee_id) REFERENCES employee (id)
        );
    '''

    create_table_sql['employee_availability'] = '''
        CREATE TABLE IF NOT EXISTS employee_availability(
            employee_id integer NOT NULL,
            availability text NOT NULL,
            PRIMARY KEY (employee_id, availability),
            FOREIGN KEY (employee_id) REFERENCES employee (id)
        );
    '''

    create_table_sql['customer'] = '''
        CREATE TABLE IF NOT EXISTS customer(
            email text PRIMARY KEY NOT NULL,
            company text NOT NULL,
            credit_limit integer NOT NULL,
            first_name text NOT NULL,
            last_name text NOT NULL,
            suffix text NOT NULL,
            unit_number integer NOT NULL,
            street_number integer NOT NULL,
            suburb text NOT NULL,
            postal_code text NOT NULL
        );
    '''
    
    create_table_sql['customer_phone_number'] = '''
        CREATE TABLE IF NOT EXISTS customer_phone_number(
            customer_email text NOT NULL,
            phone_number integer NOT NULL,
            PRIMARY KEY (customer_email, phone_number),
            FOREIGN KEY (customer_email) REFERENCES customer (email)
        );
    '''

    create_table_sql['propane_tank'] = '''
        CREATE TABLE IF NOT EXISTS propane_tank(
            serial_number int PRIMARY KEY NOT NULL,
            manufacturer text NOT NULL, 
            expiration_date text NOT NULL,
            quick_fill text NOT NULL,
            form_factor text NOT NULL,
            tare_weight text NOT NULL,
            water_capacity text NOT NULL,
            liquid_vapor text NOT NULL,
            rust_level integer,
            production_date text,
            last_visual_check_date text,
            type_of_tank text NOT NULL,
            sold_by_employee_id int,
            sold_to_customer_email text,
            sell_date text,
            FOREIGN KEY (sold_by_employee_id)
                REFERENCES employee (id),
            FOREIGN KEY (sold_to_customer_email)
                REFERENCES customer (email)
        );
    '''
 
    create_table_sql['truck'] = '''
        CREATE TABLE IF NOT EXISTS truck(
            vin int PRIMARY KEY NOT NULL,
            license_plate_number text NOT NULL,
            capacity int NOT NULL,
            passenger_limit int NOT NULL
        )
    '''


    create_table_sql['work_order'] = '''
        CREATE TABLE IF NOT EXISTS work_order(
            order_number integer NOT NULL,
            customer_email text NOT NULL,
            order_total integer NOT NULL,
            order_status text NOT NULL,
            payment_method text NOT NULL,
            rush_level text NOT NULL,
            order_date text NOT NULL,
            po_number integer NOT NULL,
            expected_completion_date text NOT NULL,
            PRIMARY KEY(
                order_number,
                customer_email
            ),
            FOREIGN KEY(customer_email)
                REFERENCES customer (email) 
        );
    '''

    create_table_sql['work_order_employee'] = '''
        CREATE TABLE IF NOT EXISTS work_order_employee(
            work_order_number integer NOT NULL,
            employee_id integer NOT NULL,
            PRIMARY KEY(
                work_order_number,
                employee_id
            ),
            FOREIGN KEY (work_order_number)
                REFERENCES work_order (order_number),
            FOREIGN KEY (employee_id)
                REFERENCES employee (id)
        );
    '''

    create_table_sql['work_order_propane_tank'] = '''
        CREATE TABLE IF NOT EXISTS work_order_propane_tank(
            work_order_number integer NOT NULL,
            propane_tank_serial_number integer NOT NULL,
            PRIMARY KEY(
                work_order_number,
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
            employee_id integer NOT NULL,
            customer_email text NOT NULL,
            serial_number integer NOT NULL,
            vin text NOT NULL,
            delivery_date text NOT NULL,
            PRIMARY KEY (
                employee_id,
                customer_email,
                vin
            ),
            FOREIGN KEY (employee_id)
                REFERENCES employee (id),
            FOREIGN KEY (customer_email)
                REFERENCES customer (email),
            FOREIGN KEY (vin)
                REFERENCES truck (vin)
        );
    '''

    for sql in create_table_sql.values():
        execute_sql(connection, sql)


def delete_tables(connection):
    table_names = [
        'employee', 'employee_qualification', 'employee_availability',
        'work_order', 'work_order_employee', 'work_order_propane_tank',
        'delivery', 'customer', 'customer_phone_number', 'propane_tank',
        'truck'
    ]

    delete_table_sql = [
        f'DROP TABLE IF EXISTS {table_name};' for table_name in table_names
    ]
    
    for sql in delete_table_sql:
        execute_sql(connection, sql)

        
def main():
    database = 'propane354.db'
    connection = create_connection(database)
    
    if (connection):
        delete_tables(connection)
        create_tables(connection)
    else:
        print('Failed to create database connection.')


if __name__ == '__main__':
    main()

    
