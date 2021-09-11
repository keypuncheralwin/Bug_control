from flask import Flask, render_template, request, redirect, session
import os
import psycopg2

from models.query import sign_up_user, check_email, get_password_hash

DB_URL = os.environ.get("DATABASE_URL", "dbname=bugger")
SECRET_KEY = os.environ.get("SECRET_KEY", "pretend key for testing only")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/login_action', methods=['POST'])
def login_action():
    email = request.form.get('email')
    password = request.form.get('password')
    if check_email(email):
        password_hash = get_password_hash(email)[0][0]
        valid = bcrypt.checkpw(password.encode(), password_hash.encode())
        if valid:
            session['email_address'] = email
            return redirect('/') 
        else:
            incorrect_login = True
            return render_template('login.html', incorrect_login=incorrect_login)    
    
    return render_template('login.html')


@app.route('/sign_action', methods=['POST'])
def signup_action():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    if password == confirm_password:
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        sign_up_user(name,email,password_hash)
        return render_template('login.html')
    else:
        incorrect_password = True
        return render_template('sign.html', incorrect_password=incorrect_password)


@app.route('/sign')
def sign():
    return render_template('sign.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/guest')
def guest():
    return render_template('bugsList.html')

@app.route('/')
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)