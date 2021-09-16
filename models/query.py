from database import sql_select, sql_write

def check_email(email):
  items = sql_select("SELECT email from users WHERE email=%s", [email])
  return items

def get_user_name(email):
  user = sql_select("SELECT name from users WHERE email=%s", [email])
  return user 

def user_by_id(id):
  user = sql_select("SELECT u.name FROM bugs b LEFT JOIN users u ON u.id = b.user_id WHERE b.id=%s", [id])
  return user

def get_user_id(email):
  user = sql_select("SELECT id from users WHERE email=%s", [email])
  return user 

def name_by_id(id):
  user = sql_select("SELECT name from users WHERE id=%s", [id])
  return user 

def sign_up_user(name, email, password_hash):
  sql_write("INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)", [name, email, password_hash])

def get_password_hash(email):
  password_hash = sql_select("SELECT password_hash from users WHERE email=%s", [email])
  return password_hash 

def all_bugs():
  items = sql_select("SELECT b.*, u.name FROM bugs b LEFT JOIN users u ON u.id = b.user_id ORDER BY b.id DESC")
  return items

def report_bug(date,title,description,priority,user_id):
  sql_write("INSERT INTO bugs (created_on, title, description, priority, user_id) VALUES (%s, %s, %s, %s, %s)", [date,title,description,priority,user_id])


def edit_bug(id):
  items = sql_select("SELECT * FROM bugs WHERE id=%s", [id])
  return items

def bug_update(updated_on,title,description,priority,updated_by,id):
  sql_write("UPDATE bugs SET title=%s, description=%s, priority=%s, updated_on=%s, updated_by=%s WHERE id=%s", [title,description,priority,updated_on,updated_by,id])

def delete_bug(id):
  sql_write("DELETE FROM bugs WHERE id=%s", [id])

def user_bug_count():
  count = sql_select("SELECT u.name, COUNT(*) AS bug_count FROM bugs b INNER JOIN users u ON u.id = b.user_id GROUP BY b.user_id, u.name;")
  return count

def total_bug_count():
  count = sql_select("SELECT COUNT(b.id)  FROM bugs b;")
  return count

def update_archive(date,title,description,resolved,user_id,archived_by):
  sql_write("INSERT INTO archive (archived_on, title, description, resolved, user_id, archived_by) VALUES (%s, %s, %s, %s, %s, %s)", [date,title,description,resolved,user_id,archived_by])

def all_archive():
  items = sql_select("SELECT * from archive")
  return items    