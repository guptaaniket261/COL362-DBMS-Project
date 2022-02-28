from asyncio.windows_events import NULL
import os
import psycopg2
from flask import Blueprint, Flask, render_template, redirect, request, flash, session
from config import credentials
from models import *
from flask_session import Session


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.secret_key = '4356528348'


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
  return redirect('/login')


@app.route('/login', methods=["GET", "POST"])
def login():
  if request.method == "POST":
    email = request.form['email']
    password = request.form['password']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM login_details WHERE login_id = %s AND password = %s", (email, password))
    user = cur.fetchone()
    if not user:
      flash("Invalid email or password")
      return redirect('/login')


    if user[4] != None:
      # session.clear()
      session['userid'] = user[4]
      return redirect('/user_{0}'.format(user[4]))
    else:
      session['companyid'] = user[5]
      print("==============================")
      print(session.get('companyid'))
      print("==============================")
      return redirect('/company_{0}'.format(user[5]))

  return render_template('loginPage.html')

@app.route('/logout')
def logout():
  session.clear()
  return redirect('/login')


@app.route('/user_register', methods=['POST', 'GET'])
def user_register():
  # print(request.form)
  if request.method == "POST":
    email = request.form['email']
    password = request.form['password']
    user_type = request.form['user_type']

    conn = get_db_connection()
    cur = conn.cursor()
    print(email)
    cur.execute("SELECT * FROM login_details WHERE login_id = '{0}'".format(email))
    user = cur.fetchone()
    if user:
      print("User already exists")
      # flash('User already exists',category='error')
      return redirect('/user_register')
    else:
      if user_type == "applicant":
        cur.execute("select max(user_id) from user_details")
        userid = cur.fetchone()[0] + 1
        cur.execute("INSERT INTO user_details VALUES (%(userid)s, NULL, NULL,NULL,NULL,NULL,NULL,NULL,%(o)s, NULL, NULL)", {'o': str(email), 'userid': userid})
        conn.commit()
        
        print("=====================")
        print(userid)
        print("=====================")

        cur.execute("select max(pid) from login_details")
        pid = cur.fetchone()[0] + 1
        cur.execute("INSERT INTO login_details VALUES (%(pid)s, %(email)s, %(password)s, 'applicant', %(userid)s, NULL)", {'email': str(email), 'password': str(password), 'userid': userid, 'pid': pid})
        conn.commit()
    return redirect('/login')
  return render_template('user_register.html')


@app.route('/user_<int:userid>', methods=['POST', 'GET'])
def user(userid):
  # print(userid, session['username'])
  if not session.get('userid'):
    return redirect('/login')
  if session.get('userid') != userid:
    return redirect('/login')
  # print(type(session.get('userid')), type(userid))
  
  return redirect('/user_{0}/0'.format(userid))


@app.route('/user_<int:userid>/<offset>', methods=["GET", "POST"])
def userpage(userid, offset):
  # print("==========================")
  # print(USER_DETAILS.firstname)
  # print("==========================")
  if not session.get('userid'):
    return redirect('/login')
  if session.get('userid') != userid:
    return redirect('/login')
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute("select * from user_details where user_id = %(o)s", {'o': userid})
  user = cur.fetchone()
  userDetail = UserDetails(user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8], user[9], user[10])

  print(request.form)
  if offset.isnumeric():
    pg = int(float(offset))
    start = int(float(offset))*10
  else:
    start = 0
    pg = 0
  if request.method == "GET":   
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

    return render_template('userPage.html', jobs = jobs, pgs = pgs, curr_pg = pg, locations = locations, companies = companies, categories = categories, user = userDetail)
  

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
    return render_template('userPage.html', jobs = jobs, pgs = [pg, pg+1, pg+2, pg+3], curr_pg = pg, locations = locations, companies = companies, categories = categories, user = userDetail)

  return redirect('/user_{0}/0'.format(userid))


@app.route('/job_apply_<int:userid>/<int:jobid>', methods=["GET", "POST"])
def applyForJob(userid, jobid):
  if not session.get('userid'):
    return redirect('/login')
  if session.get('userid') != userid:
    return redirect('/login')
  conn = get_db_connection()
  cur = conn.cursor()
  if request.method == "GET":
    print("==========================")
    print(request.form)
    print("==========================")
    cur.execute("SELECT * FROM applications WHERE job_id = %(o)s and user_id = %(u)s", {'o': jobid, 'u': userid})
    job = cur.fetchone()
    if job is None:
      cur.execute("select max(application_id) from applications")
      application_id = cur.fetchone()[0] + 1
      cur.execute("insert into applications values(%(a)s, %(j)s, %(u)s, 0)", {'a': application_id, 'u': userid, 'j': jobid})
      conn.commit()
    return redirect('/user_{0}/0'.format(userid))
  else:
    return redirect('/login')


@app.route('/applications/<jobid>')
def applications(jobid):
  # return render_template('loginPage.html')
  conn = get_db_connection()
  cur = conn.cursor()
  # TODO Query to be changed
  cur.execute("SELECT application_id, firstname, lastname, age, gender, education, email, contact, status FROM user_details NATURAL JOIN (SELECT * FROM applications WHERE  job_id = %(j_id)s))", {"j_id": jobid })
  applicants = cur.fetchall()

  return render_template('applications.html', applicants=applicants)


@app.route('/job_details_<int:userid>/<int:jobid>')
def jobDetails(jobid, userid):
  if not session.get('userid'):
    return redirect('/login')
  if session.get('userid') != userid:
    return redirect('/login')
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute("SELECT * FROM job_details WHERE job_id = %(o)s", {"o": jobid})
  job = cur.fetchone()
  cur.execute("SELECT * FROM company_details WHERE company_id = %(o)s", {"o": job[1]})
  company = cur.fetchone()
  job_detail = JobDetail(job[0], company[1], job[2], job[3], job[4], job[5], job[6], job[7], job[8], job[9], company[2], company[7], company[8])
  return render_template('job_detail.html', job_detail=job_detail, userid=userid)


@app.route('/jobsApplied_<int:userid>')
def jobs_applied(userid):
  if not session.get('userid'):
    return redirect('/login')
  if session.get('userid') != userid:
    return redirect('/login')
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute('''SELECT jobs.job_id, company_details.company_name,  
                    title, description, job_type, prerequisites, skills, 
                    pay_rate, no_positions, experience_required , location, 
                    contact, email, applications.status
                    FROM (select * from job_details where status = '1') as jobs
                    join company_details on
                    company_details.company_id = jobs.company_id 
                    join applications on
                    applications.job_id = jobs.job_id 
                    and applications.user_id = %(u)s''', {"u": userid})
  jobs = cur.fetchall()
  jobs_applied = []
  status_map = {0: "APPLICATION IN PROCESS", 1: "APPLICATION ACCEPTED", 2: "APPLICATION REJECTED"}
  for job in jobs:
    job_detail = JobDetail(job[0], job[1], job[2], job[3], job[4], job[5], job[6], job[7], job[8], job[9], job[10], job[11], job[12], status_map[job[13]])
    jobs_applied.append(job_detail)

  return render_template('jobsApplied.html', jobs_applied=jobs_applied, user_id=userid)


@app.route('/user_profile')
def get():
  return render_template('user_profile.html')

@app.route('/company_<cmpid>', methods=["GET", "POST"])
def cmppage(cmpid):
  if not session.get('companyid'):
    return redirect('/login')
  if int(session.get('companyid')) != int(cmpid):
    return redirect('/login')

  if request.method == "GET":
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM company_details WHERE company_id = %(o)s", {"o": cmpid})
    company = cur.fetchone()
    company_detail = companyDetails(company[0], company[1], company[2], company[3], company[4], company[5], company[6], company[7], company[8], company[9])
    cur.execute("SELECT * FROM job_details WHERE company_id = %(c)s", {"c": cmpid})
    jobs = cur.fetchall()
    job_details = []
    for job in jobs:
      job_details.append(JobDetail(job[0], company[1], job[2], job[3], job[4], job[5], job[6], job[7], job[8], job[9], company[2], company[7], company[8]))
    return render_template('companyPage.html', jobs = job_details, company_detail = company_detail)
  
  if request.method == "POST":
    print("==========================")
    print("Handling POST request")
    print("==========================")
    # TODO Needs to be changed
    return redirect('/user/0')


@app.route('/company_profile')
def getcompany_profile():
  return render_template('company_profile.html')


@app.route('/postjob')
def createjob():
  return render_template('postJob.html')




if __name__ == '__main__':
  app.run(debug=True)