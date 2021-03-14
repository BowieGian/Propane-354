import pandas as pd
import sqlite3
from sqlite3 import Error
from our_sql import *


def main():
    database = 'propane354.db'

    connection = create_connection(database)
    
    if (connection):
        # insert an employee into the `employee` table  
        #employee1 = ('johndoe@gmail.com', 'John', 'Doe', 'SomeSuffix', '2021-03-05', 42000, 'Laborer')
        #insert_employee(connection, employee1)

        # insert a qualification into the `employee_qualification` table
        #employee1_qualifications = (1, 'Certified Inspector')
        #insert_employee_qualification(connection, employee1_qualifications)

        # view all tables - uncomment line in the insert function to commit changes
        table_names = [
            'employee', 'employee_qualification', 'employee_availability',
            'work_order', 'work_order_employee', 'work_order_propane_tank',
            'delivery', 'customer', 'customer_phone_number', 'propane_tank',
            'truck'
        ]

        tables = {}
        for table_name in table_names:
            tables[table_name] = pd.read_sql(
                f'SELECT * FROM {table_name};',
                connection
            )
            print(tables[table_name])
            print()
    else:
        print("Failed to create database connection.")


if __name__ == '__main__':
    main()
        
