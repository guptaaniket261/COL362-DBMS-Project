import os
import psycopg2
from flask import Flask, render_template
from config import credentials


app = Flask(__name__)

def get_db_connection():
    """
    Returns a connection to the database
    """
    conn = psycopg2.connect(
      host = credentials['host'],
      database = credentials['database'],
      user = credentials['user'],
      password = credentials['password']
    )

    return conn

@app.route('/')
def index():
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute("SELECT * FROM drivers limit 10")
  drivers = cur.fetchall()
  return render_template('index.html', drivers=drivers)

@app.route('/profile')
def get():
  # conn = get_db_connection()
  # cur = conn.cursor()
  # cur.execute("SELECT * FROM drivers limit 10")
  # drivers = cur.fetchall()
  return render_template('user_profile.html')


if __name__ == '__main__':
  app.run(debug=True)