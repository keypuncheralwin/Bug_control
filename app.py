from flask import Flask, render_template, request, redirect, session
import os
import psycopg2
import bcrypt

from models.query import sign_up_user, check_email, get_password_hash, all_bugs, get_user_name, get_user_id, user_by_id, report_bug, edit_bug, bug_update, user_bug_count, update_archive, all_archive, delete_bug, name_by_id
from datetime import date  

DB_URL = os.environ.get("DATABASE_URL", "dbname=bugger")
SECRET_KEY = os.environ.get("SECRET_KEY", "pretend key for testing only")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/archives')
def archives():
    archive_all = all_archive()
    if session:
        email = session['email_address']
        full_name = get_user_name(email)[0][0]
        first_name = full_name.split()[0]
    else:
        first_name = 'Guest'
    return render_template('archives.html', archives=archive_all, name=first_name)

@app.route('/archive_bug_action', methods=['POST'])
def archive_bug_action():
    today = date.today()
    email = session['email_address']
    user_id = get_user_id(email)[0][0]
    full_name = get_user_name(email)[0][0]
    created_on = today
    resolved = request.form.get('resolved')
    title = request.form.get('title')
    description = request.form.get('description')
    id = request.form.get('bug_id')
    update_archive(created_on,title,description,resolved,user_id,full_name)
    delete_bug(id)
    return redirect('/archives')

@app.route('/edit_action', methods=['POST'])
def edit_action():
    email = session['email_address']
    updated_by = get_user_id(email)[0][0]
    today = date.today()
    updated_on = today
    priority = request.form.get('priority')
    title = request.form.get('title')
    description = request.form.get('description')
    id = request.form.get('bug_id')
    bug_update(updated_on,title,description,priority,updated_by,id)
    return redirect('/bugs_list')    

@app.route('/archive_bug/<id>')
def archive(id):
    user_name = user_by_id(id)[0][0]
    results = edit_bug(id)[0]
    title = results[2]
    description = results[3]
    date = results[1]
    email = session['email_address']
    full_name = get_user_name(email)[0][0]
    first_name = full_name.split()[0]

    return render_template('archiveBug.html', date=date, description=description, title=title, id=id, name=first_name, user_name=user_name)
    

@app.route('/view/<id>')
def view(id):
    created_by = user_by_id(id)[0][0] #we're getting the  user who created the post by the bug_id
    results = edit_bug(id)[0]
    title = results[2]
    description = results[3]
    priority = results[4]
    date = results[1]
    if results[6]:
        updated_on = results[6]
        updated_by = results[7]
        updated_user = name_by_id(updated_by)[0][0]
    else:
        updated_on = False
        updated_user = False
        
    if session:
        email = session['email_address']
        full_name = get_user_name(email)[0][0]
        first_name = full_name.split()[0]
    else:
        first_name = 'Guest'
    return render_template('viewBug.html', date=date, priority=priority, description=description, title=title, id=id, name=first_name, created_by=created_by, updated_on=updated_on, updated_user=updated_user)

@app.route('/edit/<id>')
def edit(id):
    created_by = user_by_id(id)[0][0]
    results = edit_bug(id)[0]
    title = results[2]
    description = results[3]
    priority = results[4]
    date = results[1]
    if results[6]:
        updated_on = results[6]
        updated_by = results[7]
        updated_user = name_by_id(updated_by)[0][0]
    else:
        updated_on = False
        updated_user = False
    
    email = session['email_address']
    full_name = get_user_name(email)[0][0]
    first_name = full_name.split()[0]
    
    
    return render_template('editBug.html', date=date, priority=priority, description=description, title=title, name=first_name, id=id, created_by=created_by, updated_on=updated_on, updated_user=updated_user)


@app.route('/report_action', methods=['POST'])
def report_action():
    date = request.form.get('date')
    priority = request.form.get('priority')
    title = request.form.get('title')
    description = request.form.get('description')
    if session:
        email = session['email_address']
        user_id = get_user_id(email)[0][0]
        full_name = get_user_name(email)[0][0]
        print(user_id)
        report_bug(date,title,description,priority,user_id)
    return redirect('/bugs_list')

@app.route('/report')
def report():
    today = date.today()
    print(today)
    if session:
        email = session['email_address']
        full_name = get_user_name(email)[0][0]
        first_name = full_name.split()[0]
        print(first_name)
    else:
        first_name = 'Guest'
    return render_template('report.html', today=today, name=first_name) 

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/login_action', methods=['POST'])
def login_action():
    email = request.form.get('email')
    password = request.form.get('password')
    if check_email(email):
        password_hash = get_password_hash(email)[0][0]
        valid = bcrypt.checkpw(password.encode(), password_hash.encode())
        if valid:
            session['email_address'] = email
            return redirect('/dash') 
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

@app.route('/bugs_list')
def bugs_list():
    bugs = all_bugs()
    if session:
        email = session['email_address']
        full_name = get_user_name(email)[0][0]
        first_name = full_name.split()[0]
        print(first_name)
    else:
        first_name = 'Guest'
    return render_template('bugsList.html', bugs=bugs, name=first_name)

@app.route('/dash')
def dash():
    bug_count = user_bug_count()
    user = []
    count = []
    for bug in bug_count:
        user.append(bug[0])
        count.append(bug[1])

    if session:
        email = session['email_address']
        full_name = get_user_name(email)[0][0]
        first_name = full_name.split()[0]
        print(first_name)
    else:
        first_name = 'Guest'


    return render_template('dash.html', bug_count=bug_count, name=first_name)

@app.route('/')
def main():
    return render_template('index.html')

     

if __name__ == "__main__":
    app.run(debug=True)