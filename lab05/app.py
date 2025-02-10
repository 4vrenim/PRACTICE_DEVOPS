from flask import Flask
import psycopg2
import os

app = Flask(__name__)

# Cấu hình kết nối cơ sở dữ liệu
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_NAME = os.environ.get('DB_NAME', 'flaskdb')
DB_USER = os.environ.get('DB_USER', 'user')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')

# Kết nối đến PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

@app.route('/')
def hello_world():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT message FROM greetings LIMIT 1;')
    message = cur.fetchone()[0]
    cur.close()
    conn.close()
    return f'Greeting from DB: {message}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

