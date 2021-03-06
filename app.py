from flask import Flask, render_template, request, redirect, session
import os
import psycopg2
import bcrypt

from models.query import sign_up_user, check_email, get_password_hash, all_bugs, get_user_name, get_user_id, user_by_id, report_bug, edit_bug, bug_update, user_bug_count, update_archive, all_archive, delete_bug, name_by_id,count_priority, total_bug_count, total_resolved, total_bug_reported, archive_by_id, total_archive
from datetime import date  

DB_URL = os.environ.get("DATABASE_URL", "dbname=bugger")
SECRET_KEY = os.environ.get("SECRET_KEY", "pretend key for testing only")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/view_archive/<id>')
def view_archive(id):
    results = archive_by_id(id)[0]
    archived_on = results[1]
    title = results[2]
    description = results[3]
    resolve = results[4]
    archived_by = results[6]
    if session:
        email = session['email_address']
        full_name = get_user_name(email)[0][0]
        first_name = full_name.split()[0]
    else:
        first_name = 'Guest'

    return render_template('viewArchive.html', name=first_name, archived_on=archived_on, title=title, description=description, resolve=resolve, archived_by=archived_by)

#shows all archives in table
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


#archiving a specific bug, gets the details of the bug by it's id and deletes it from the bugs databse and inserts it into the archive database
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

#updating a specific bug, gets the details of the bug by it's id and updates it
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

#rendering the archive page
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
    
#renders a read only version of a specific bug by id
@app.route('/view/<id>')
def view(id):
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
            return render_template('index.html', incorrect_login=incorrect_login)    
    
    return render_template('index.html')


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
    priority_count = count_priority()[0]
    urgent_bugs = priority_count[2]
    total_bugs = total_bug_count()[0][0]
    total_resolved_bugs = total_resolved()[0][0]
    archive_count = total_archive()[0][0]

    if session:
        email = session['email_address']
        full_name = get_user_name(email)[0][0]
        first_name = full_name.split()[0]
        current_user_id = get_user_id(email)[0][0]
        bugs_reported = total_bug_reported(current_user_id)[0][0]
    else:
        first_name = 'Guest'
        bugs_reported = 0


    return render_template('dash.html', bug_count=bug_count, name=first_name, priority_count=priority_count, urgent_bugs=urgent_bugs, total_bugs =total_bugs, total_resolved=total_resolved_bugs, bugs_reported=bugs_reported, archive_count=archive_count )

@app.route('/')
def main():
    return render_template('index.html')

     

if __name__ == "__main__":
    app.run(debug=True)