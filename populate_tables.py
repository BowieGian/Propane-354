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
        ('12345', 'Manufacturer1', '12-08-2022', 'yes', 'tall', 4.7, 48, 'liquid', None , None, None, 'Aluminium', 1, 'JohnSmith@bigCompany.com', '13-03-2021'),
        ('24680', 'Manufacturer1', '16-11-2023', 'yes', 'squat', 10, 64, 'vapour', None, '19-06-2020', '13-03-2021', 'Fiber', 2, 'WalterBiggins@smallCompany.com', '13-03-2021'),
        ('13579', 'Manufacturer1', '13-01-2024', 'no', 'tall', 6, 50, 'vapour', 5, None, None, 'Steel', 3, 'AlbertWoo@smallCompany.com', '13-03-2021'),
        ('12460', 'Manufacturer2', '22-05-2025', 'yes', 'squat', 8, 96, 'liquid', None, None, None, 'Aluminium', 4, 'SamYang@smallCompany.com', '13-03-2021'),
        ('00001', 'Manufacturer2', '25-03-2026', 'no', 'tall', 4.7, 48, 'liquid', None, None, None, 'Aluminium', 5, 'SarahBrown@smallCompany.com', '13-03-2021')
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


def populate_tables(connection):
    populate_employee(connection)
    populate_employee_qualification(connection)
    populate_employee_availability(connection)
    populate_customer(connection)
    populate_customer_phone(connection)
    populate_propane_tank(connection)
    populate_truck(connection)


def main():
    database = 'propane354.db'
    connection = create_connection(database)
    
    if (connection):
        populate_tables(connection)
    else:
        print('Failed to create database connection.')


if __name__ == '__main__':
    main()
