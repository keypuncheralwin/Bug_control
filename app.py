from flask import Flask
import os
import psycopg2

DB_URL = os.environ.get("DATABASE_URL", "dbname=bugger")
SECRET_KEY = os.environ.get("SECRET_KEY", "pretend key for testing only")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('SELECT * FROM users') # Query to check that the DB connected
    results = cur.fetchall()
    conn.close()
    return f'Hello, world Alwin! {results}'

if __name__ == "__main__":
    app.run(debug=True)