import sqlite3
from sqlite3 import Error
from our_sql import *


def populate_employee(connection):
    employees = [
        ('john.doe354@gmail.com', 'John', 'Doe', 'Mr.', '2021-03-05', 42000, 'Laborer'),
        ('brett.ray354@gmail.com', 'Brett', 'Ray', 'Mr.', '2018-03-13', 42000, 'Driver'),
        ('julian.terry354@gmail.com', 'Julian', 'Terry', 'Mr.', '2021-01-01', 60000, 'Accounting/HR'),
        ('randy.braum354@gmail.com', 'Randy', 'Braum', 'Mr.', '2019-12-20', 72000, 'Management'),
        ('lilith.ellwood354@gmail.com', 'Lilith', 'Ellwood', 'Ms.', '2020-02-13', 45000, 'Retail')
    ]
    for employee in employees:
        insert_employee(connection, employee)


def populate_employee_qualification(connection):
    qualifications = [
        (1, 'Certified Inspector'),
        (2, 'Class 3 Licence'),
        (3, 'Chartered Professional Accountant'),
        (3, 'Certified Management Accountant'),
        (5, 'Certified in Retail Management')
    ]
    for qualification in qualifications:
        insert_employee_qualification(connection, qualification)


def populate_employee_availability(connection):
    availabilities = [
        (1, 'Monday'),
        (1, 'Wednesday'),
        (1, 'Friday'),
        (2, 'Monday'),
        (2, 'Tuesday'),
        (2, 'Wednesday'),
        (2, 'Thursday'),
        (2, 'Friday'),
        (3, 'Tuesday'),
        (3, 'Thursday')
    ]
    for availability in availabilities:
        insert_employee_availability(connection, availability)


def populate_customer(connection):
    customers = [
        ('JohnSmith@bigCompany.com', 'bigCompany', 25000, 'John', 'Smith', 'Sr.', 125, 25, 'Big St.', '555 555'),
        ('WalterBiggins@smallCompany.com', 'smallCompany', 15000, 'Walter', 'Biggins', None, 493, 29, 'White Ave.', '934 135'),
        ('AlbertWoo@smallCompany.com', 'smallCompany', 10000, 'Albert', 'Woo', None, 21, 105, 'Kings Ave.', '456 231'),
        ('SamYang@smallCompany.com', 'bigCompany', 60000, 'Sam', 'Yang', None, 21, 452, 'Yukon St.', '862 456'),
        ('SarahBrown@smallCompany.com', 'bigCompany', 30000, 'Sarah', 'Brown', None, 500, 45, 'Brookes Ave.', '316 789')
    ]
    for customer in customers:
        insert_customer(connection, customer)


def populate_customer_phone(connection):
    customer_phone_numbers = [
        ('JohnSmith@bigCompany.com', 1234567890),
        ('JohnSmith@bigCompany.com', 1234567891),
        ('WalterBiggins@smallCompany.com', 1234567892),
        ('AlbertWoo@smallCompany.com', 1234567893),
        ('SamYang@smallCompany.com', 1234567894),
        ('SarahBrown@smallCompany.com', 1234567895)
    ]
    for customer_phone_number in customer_phone_numbers:
        insert_customer_phone_number(connection, customer_phone_number)


def populate_propane_tank(connection):
    propane_tanks = [
        ('12345', 'Manufacturer1', '2022-08-12', 'yes', 'tall', 4.7, 48, 'liquid', None , None, None, 'Aluminium', 1, 'JohnSmith@bigCompany.com', '2021-03-13'),
        ('24680', 'Manufacturer1', '2023-11-16', 'yes', 'squat', 10, 64, 'vapour', None, '2020-06-19', '13-03-2021', 'Fiber', 2, 'WalterBiggins@smallCompany.com', '2021-03-13'),
        ('13579', 'Manufacturer1', '2024-01-13', 'no', 'tall', 6, 50, 'vapour', 5, None, None, 'Steel', 3, 'AlbertWoo@smallCompany.com', '2021-03-13'),
        ('12460', 'Manufacturer2', '2025-05-22', 'yes', 'squat', 8, 96, 'liquid', None, None, None, 'Aluminium', 4, 'SamYang@smallCompany.com', '2021-03-13'),
        ('00001', 'Manufacturer2', '2026-03-25', 'no', 'tall', 4.7, 48, 'liquid', None, None, None, 'Aluminium', 5, 'SarahBrown@smallCompany.com', '2021-03-13')
    ]
    for propane_tank in propane_tanks:
        insert_propane_tank(connection, propane_tank)


def populate_truck(connection):
    trucks = [
        ('2BG10509500821682', 'AAA 001', 5000, 2),
        ('2BG10509500821542', 'AAA 002', 4000, 2),
        ('2BG10509500821321', 'AAA 003', 7000, 2),
        ('2BG10509500821132', 'AAA 004', 3000, 2),
        ('2BG10509500821246', 'AAA 005', 5000, 2)
    ]
    for truck in trucks:
        insert_truck(connection, truck);


def populate_work_order(connection):
    work_orders = [
        (1, 'JohnSmith@bigCompany.com', 2475, 'Complete', 'Credit', 'Express', '2021-03-04', 1234, '2021-03-05'),
        (2, 'WalterBiggins@smallCompany.com', 759, 'In Progress', 'Cheque', 'Express', '2021-03-06', 1235, '2021-03-13'),
        (3, 'AlbertWoo@smallCompany.com', 690, 'In Progress', 'Debit', 'Standard', '2021-03-13', 1236, '2021-03-27'),
        (4, 'SamYang@smallCompany.com', 245, 'On Hold', 'Cash', 'Standard', '2021-03-13', 1237, None),
        (5, 'SarahBrown@smallCompany.com', 895, 'On Hold', 'Credit', 'Standard', '2021-03-13', 1238, None)
    ]
    for work_order in work_orders:
        insert_work_order(connection, work_order)


def populate_work_order_employee(connection):
    work_order_employees = [
        (1, 1),
        (2, 1),
        (2, 2),
        (3, 1),
        (3, 2)
    ]
    for work_order_employee in work_order_employees:
        insert_work_order_employee(connection, work_order_employee)


def populate_work_order_propane_tank(connection):
    work_order_propane_tanks = [
        (1, '12345'),
        (2, '24680'),
        (3, '13579'),
        (4, '12460'),
        (5, '00001')
    ]
    for work_order_propane_tank in work_order_propane_tanks:
        insert_work_order_propane_tank(connection, work_order_propane_tank)


def populate_delivery(connection):
    deliveries = [
        ('12345', 2, '2BG10509500821132', 'JohnSmith@bigCompany.com', '2021-03-13'),
        ('24680', 2, '2BG10509500821132', 'WalterBiggins@smallCompany.com', '2021-03-13'),
        ('13579', 2, '2BG10509500821132', 'AlbertWoo@smallCompany.com', '2021-03-14'),
        ('12460', 2, '2BG10509500821132', 'SamYang@smallCompany.com', '2021-03-15'),
        ('00001', 2, '2BG10509500821132',  'SarahBrown@smallCompany.com', '2021-03-17')
    ]
    for delivery in deliveries:
        insert_delivery(connection, delivery)


def populate_tables(connection):
    populate_employee(connection)
    populate_employee_qualification(connection)
    populate_employee_availability(connection)
    populate_customer(connection)
    populate_customer_phone(connection)
    populate_propane_tank(connection)
    populate_truck(connection)
    populate_work_order(connection)
    populate_work_order_employee(connection)
    populate_work_order_propane_tank(connection)
    populate_delivery(connection)
    

def main():
    database = 'propane354.db'
    connection = create_connection(database)
    
    if (connection):
        populate_tables(connection)
    else:
        print('Failed to create database connection.')


if __name__ == '__main__':
    main()
