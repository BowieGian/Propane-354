from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['get', 'post'])
def index():
    if request.method == 'post':
        username = request.form['username']
        id = request.form['id']
        return redirect('/')
    else:
        return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
