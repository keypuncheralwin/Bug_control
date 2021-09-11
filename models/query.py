from database import sql_select, sql_write

def check_email(email):
  items = sql_select("SELECT email from users WHERE email=%s", [email])
  return items

def get_user_name(email):
  user = sql_select("SELECT name from users WHERE email=%s", [email])
  return user 

def sign_up_user(name, email, password_hash):
    sql_write("INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)", [name, email, password_hash])

def get_password_hash(email):
  password_hash = sql_select("SELECT password_hash from users WHERE email=%s", [email])
  return password_hash 