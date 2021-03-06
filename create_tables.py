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

    
