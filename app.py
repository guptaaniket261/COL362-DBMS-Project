import os
import psycopg2
from flask import Flask, render_template, redirect, request
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
@app.route('/user_profile')
def get():
  # conn = get_db_connection()
  # cur = conn.cursor()
  # cur.execute("SELECT * FROM drivers limit 10")
  # drivers = cur.fetchall()
  return render_template('user_profile.html')

@app.route('/company_profile')
def getcompany_profile():
  return render_template('company_profile.html')

@app.route('/login', methods=["GET", "POST"])
def login():
  print(request.form)
  return render_template('loginPage.html')

@app.route('/company')
def companypage():
  return render_template('companyPage.html')

@app.route('/postjob')
def createjob():
  return render_template('postJob.html')

def user():
  return redirect('/user/0')

@app.route('/user/<offset>', methods=["GET", "POST"])
def userpage(offset):
  print(request.form)
  if request.method == "GET":
    conn = get_db_connection()
    cur = conn.cursor()
    if offset.isnumeric():
      pg = int(float(offset))
      start = int(float(offset))*10
    else:
      start = 0
      pg = 0
    cur.execute("SELECT * FROM job_details limit 10 offset %(o)s", {"o": start})
    jobs = cur.fetchall()
    cur.execute("Select company_id, company_name, location from company_details")
    companies = cur.fetchall()
    return render_template('userPage.html', jobs = jobs, pgs = [pg, pg+1, pg+2, pg+3], companies = companies)
  
  if request.method == "POST":
    print("==========================")
    print("Handling POST request")
    print("==========================")
    # conn = get_db_connection()
    # cur = conn.cursor()
    # cur.execute("INSERT INTO applications (user_id, job_id) VALUES (%(u_id)s, %(j_id)s)", {"u_id": request.form['user_id'], "j_id": request.form['job_id']})
    # conn.commit()
    return redirect('/user/0')


if __name__ == '__main__':
  app.run(debug=True)