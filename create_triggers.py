# referenced https://www.sqlitetutorial.net/sqlite-trigger/
import sqlite3
from sqlite3 import Error
from our_sql import create_connection


def execute_sql(connection, sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
    except Error as e:
        print(e)


def create_triggers(connection):
    create_trigger_sql = {}

    # trigger_name: (table_name, column_name)
    date_trigger_values = {
        'validate_employee_start_date': ('employee', 'start_date'),
        'validate_propane_tank_expiration_date': ('propane_tank', 'expiration_date'),
        'validate_work_order_order_date': ('work_order', 'order_date'),
        'validate_delivery_date': ('delivery', 'delivery_date')
    }

    for trigger_name, (table_name, column_name) in date_trigger_values.items():
        create_trigger_sql[trigger_name] = f'''
            CREATE TRIGGER {trigger_name}
            BEFORE INSERT ON {table_name}
            BEGIN
                SELECT CASE 
                    WHEN NEW.{column_name} NOT LIKE '____-__-__'
                    THEN RAISE (ABORT, 'Invalid date. Date should be in yyyy-mm-dd format.')
                END;
            END;
        '''

    # TODO - add
    # propane tank - last visual check date, sell date for propane tank (IS NOT NULL AND NOT LIKE)
    # work order - expected completion date
                                                     

    # does not flag yyyy-dd-mm or invalid years, months or days
    create_trigger_sql['validate_employee_start_date'] = '''
        CREATE TRIGGER validate_employee_start_date
        BEFORE INSERT ON employee
        BEGIN
            SELECT CASE 
                WHEN NEW.start_date NOT LIKE '____-__-__'
                THEN RAISE (ABORT, 'Invalid date. Date should be in yyyy-mm-dd format.')
            END;
        END;
    '''
    
    email_trigger_values = {
        'validate_employee_email': ('employee', 'email'),
        'validate_customer_email': ('customer', 'email'),
    }
                                                     
    for trigger_name, (table_name, column_name) in email_trigger_values.items():
        create_trigger_sql[trigger_name] = f'''
            CREATE TRIGGER {trigger_name}
            BEFORE INSERT ON {table_name}
            BEGIN
                SELECT CASE 
                    WHEN NEW.{column_name} NOT LIKE '%_@_%'
                    THEN RAISE (ABORT, 'Invalid email.')
                END;
            END;
        '''

    for sql in create_trigger_sql.values():
        execute_sql(connection, sql)


def delete_triggers(connection):
    trigger_names = [
        'validate_employee_start_date', 
        
        'validate_employee_email',
        'validate_customer_email',
        'validate_customer_phone_email',
        'validate_propane_tank_sold_to_customer_email',
        'validate_work_order_customer_email',
        'validate_delivery_customer_email'
    ]

    delete_trigger_sql = [
        f'DROP TRIGGER IF EXISTS {trigger_name};' for trigger_name in trigger_names
    ]
    
    for sql in delete_trigger_sql:
        execute_sql(connection, sql)

        
def main():
    database = 'propane354.db'
    connection = create_connection(database)
    
    if (connection):
        delete_triggers(connection)
        create_triggers(connection)
    else:
        print('Failed to create database connection.')


if __name__ == '__main__':
    main()

    
