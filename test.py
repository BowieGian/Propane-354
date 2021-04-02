import pandas as pd
import sqlite3
from sqlite3 import Error
from our_sql import *


def main():
    database = 'propane354.db'

    connection = create_connection(database)
    
    if (connection):
        # view all tables
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
            
        # test triggers
        invalid_employees = [
            ('notARealEmail', 'John', 'Doe', 'Mr.', '2021-03-05', 42000, 'Laborer'),         # test email trigger
            ('brett.ray354@gmail.com', 'Brett', 'Ray', 'Mr.', '12-03-2021', 42000, 'Driver') # test start_date trigger
        ]
        
        for invalid_employee in invalid_employees:
            insert_employee(connection, invalid_employee)
        
    else:
        print("Failed to create database connection.")


if __name__ == '__main__':
    main()
        
