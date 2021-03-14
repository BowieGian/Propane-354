from flask import Flask, render_template, url_for, request, redirect
import pandas as pd
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def index():
    database = 'propane354.db'
    connection = create_connection(database)

    if (connection):
        # insert an employee into the `employee` table  
        employee1 = ('John', 'Doe', 'SomeSuffix', '2021-03-05', 42000, 'Laborer')
        insert_employee(connection, employee1)
        employee2 = ('Bob', 'Smith', 'Mr.', '2021-01-05', 40000, 'Laborer')
        insert_employee(connection, employee2)

        # insert a qualification into the `employee_qualification` table
        employee1_qualifications = (1, 'Certified Inspector')
        insert_employee_qualification(connection, employee1_qualifications)
        employee2_qualifications = (2, 'Certified Inspector')
        insert_employee_qualification(connection, employee2_qualifications)

        cursor = connection.cursor()
    else:
        return "Failed to create database connection."

    if request.method == 'POST':
        first_name = request.form['first_name']
        id = request.form['id']

        # find if login exists
        if cursor.execute('SELECT id FROM employee WHERE first_name = ? AND id = ?', (first_name, id,)).fetchone():
            return redirect(url_for('home'))
        else:
            return redirect('/')

    else:
        employees = cursor.execute('SELECT first_name FROM employee').fetchall();
        return render_template('login.html', employees=employees)

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return 'Post'
    else:
        return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
