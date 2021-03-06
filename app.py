from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///propane354.db'
db = SQLAlchemy(app)

#class Employee(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    #~~~Finish Employee Columns Here~~~

@app.route('/')
def index():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True)
