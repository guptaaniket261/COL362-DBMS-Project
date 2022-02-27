import os
import psycopg2
from flask import Blueprint, Flask, render_template, redirect, request
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


@app.route('/user_register', methods=['POST', 'GET'])
def user_register():
  return render_template('user_register.html')

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


@app.route('/user')
def user():
  return redirect('/user/0')

  

@app.route('/user/<offset>', methods=["GET", "POST"])
def userpage(offset):
  print(request.form)
  if offset.isnumeric():
      pg = int(float(offset))
      start = int(float(offset))*10
  else:
    start = 0
    pg = 0
  if request.method == "GET":
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""SELECT job_id, company_details.company_name, location, 
                  title, description, job_type, prerequisites, skills, 
                  pay_rate, no_positions, experience_required 
                  FROM (select * from job_details where status = '1' limit 10 offset %(o)s) as jobs
                  join company_details on
                  company_details.company_id = jobs.company_id""", {"o": start})    
    
    jobs = cur.fetchall()

    cur.execute("""select count(*) from job_details where status = '1'""")
    total_jobs = cur.fetchone()[0]

    cur.execute("SELECT distinct(location) FROM company_details")
    locations = cur.fetchall()

    cur.execute("SELECT distinct(company_name) FROM company_details")
    companies = cur.fetchall()

    cur.execute("SELECT distinct(skills) FROM job_details")
    categories = cur.fetchall()
    
    mxPg = int((total_jobs+9)/10)
    pgs = [pg-3]
    
    for i in range(pg-2, pg+3):
      if i >= 0 and i<mxPg:
        pgs.append(i)

    return render_template('userPage.html', jobs = jobs, pgs = pgs, curr_pg = pg, locations = locations, companies = companies, categories = categories)
  

  if request.method == "POST":
    print("==========================")
    print("Handling POST request")
    print(request.form)
    print("==========================")
    conditions = []
    if request.form.get('job-type') != "--":
      conditions.append("job_type = '{}'".format(request.form.get('job-type')))
    if request.form.get('job-location') != "--":
      conditions.append("location = '{}'".format(request.form.get('job-location')))
    if request.form.get('company') != "--":
      conditions.append("company_name = '{}'".format(request.form.get('company')))
    if request.form.get('job-category') != "--":
      conditions.append("skills = '{}'".format(request.form.get('job-category')))

    condition_str = " and ".join(conditions)
    print(condition_str)

    conn = get_db_connection()
    cur = conn.cursor()

    if(condition_str == ""):
      cur.execute("""SELECT job_id, company_details.company_name, location, 
                  title, description, job_type, prerequisites, skills, 
                  pay_rate, no_positions, experience_required 
                  FROM (select * from job_details where status = '1' limit 10 offset %(o)s) as jobs
                  join company_details on
                  company_details.company_id = jobs.company_id""", {"o": start})    
    else:
      cur.execute("""SELECT job_id, company_details.company_name, location, 
                    title, description, job_type, prerequisites, skills, 
                    pay_rate, no_positions, experience_required 
                    FROM (select * from job_details where status = '1') as jobs
                    join company_details on
                    company_details.company_id = jobs.company_id 
                    and {}""".format(condition_str))
                
    jobs = cur.fetchall()

    cur.execute("SELECT distinct(location) FROM company_details order by location")
    locations = cur.fetchall()

    cur.execute("SELECT distinct(company_name) FROM company_details order by company_name")
    companies = cur.fetchall()

    cur.execute("SELECT distinct(skills) FROM job_details")
    categories = cur.fetchall()
    pg = -1
    return render_template('userPage.html', jobs = jobs, pgs = [pg, pg+1, pg+2, pg+3], curr_pg = pg, locations = locations, companies = companies, categories = categories)

  return redirect('/user/0')




if __name__ == '__main__':
  app.run(debug=True)