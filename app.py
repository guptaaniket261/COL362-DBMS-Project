import os
import psycopg2
from flask import Flask, render_template, redirect
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
  #conn = get_db_connection()
  #cur = conn.cursor()
  #cur.execute("SELECT * FROM drivers limit 10")
  #drivers = cur.fetchall()
  #return render_template('index.html', drivers=drivers)  WHERE company_name = '{companyName}'
  return "Hello world"

@app.route('/applications/<jobid>')
def applications(jobid):
  # return render_template('loginPage.html')
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute("SELECT * FROM job_details WHERE job_id = %(j_id)s", {"j_id": jobid })
  jobRecord = cur.fetchall()

  cur.execute("SELECT * FROM user_details WHERE user_id IN (SELECT user_id FROM applications WHERE job_id = %(j_id)s)", {"j_id": jobid })
  appRecords = cur.fetchall()
  jobRecord.append(appRecords)
  print(jobRecord)
  return render_template('job-applications.html', jobAppRecord=jobRecord)

@app.route('/company-profile/<companyName>')
def companyProfilePage(companyName):
  print(companyName)
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute("SELECT * FROM company_details WHERE company_name = %(c_name)s", {"c_name": companyName })
  companyRecord = cur.fetchall()
  print(companyRecord)
  cur.execute("SELECT * FROM job_details WHERE company_id = %(c_id)s", {"c_id": companyRecord[0][0] })
  jobsRecord = cur.fetchall()
  print(jobsRecord)
  companyRecord.append(jobsRecord)
  return render_template('company-profile-page.html', companyRecord=companyRecord)
@app.route('/login')
def login():
  return render_template('loginPage.html')

@app.route('/user')
def userpage():
  return render_template('userPage.html')
if __name__ == '__main__':
  app.run(debug=True)