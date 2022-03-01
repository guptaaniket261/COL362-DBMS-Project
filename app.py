from math import exp
import os, random
import psycopg2
from flask import Blueprint, Flask, render_template, redirect, request, flash, session
from config import credentials
from models import *
from flask_session import Session

img_map = {1:"1.jpeg", 2:"2.jpeg", 3:"3.jpg", 4:"4.png", 5:"5.jpg", 6:"company.png"}


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
      password = credentials['password'],
      port = credentials['port']
    )
    return conn


@app.route('/')
def index():
  return redirect('/login')


@app.route('/login', methods=["GET", "POST"])
def login():
  print(request.method)
  if request.method == "POST":
    email = request.form['email']
    password = request.form['password']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM login_details WHERE login_id = %s AND password = %s", (email, password))
    
    user = cur.fetchone()
    if not user:
      flash("Invalid email or password", category='error')
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
      # print("User already exists")
      flash('Email id already registered',category='error')
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
  if not session.get('userid'):
    return redirect('/login')
  if session.get('userid') != userid:
    return redirect('/login')  
  return redirect('/user_{0}/0'.format(userid))


@app.route('/user_<int:userid>/<offset>', methods=["GET", "POST"])
def userpage(userid, offset):
  if not session.get('userid'):
    return redirect('/login')
  if session.get('userid') != userid:
    return redirect('/login')
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute("select * from user_details where user_id = %(o)s", {'o': userid})
  user = cur.fetchone()
  userDetail = UserDetails(user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8], user[9], user[10])
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
                  company_details.company_id = jobs.company_id and
                  job_id not in (select job_id from applications where user_id=%(u)s)""", {"o": start, "u": userid})  
    
    jobs = cur.fetchall()
    cur.execute("""select count(*) from job_details where status = '1'""")
    total_jobs = cur.fetchone()[0]
    imgs = [img_map[random.randint(1,6)] for i in range(len(jobs))]

    cur.execute("SELECT distinct(location) FROM company_details")
    locations = cur.fetchall()
    #sort locations by alphabetical order
    locations.sort(key=lambda x: x[0])


    cur.execute("SELECT distinct(company_name) FROM company_details")
    companies = cur.fetchall()

    cur.execute("SELECT distinct(skills) FROM job_details")
    categories = cur.fetchall()
    
    mxPg = int((total_jobs+9)/10)
    pgs = [pg-3]
    
    for i in range(pg-2, pg+3):
      if i >= 0 and i<mxPg:
        pgs.append(i)

    return render_template('userPage.html', imgs=imgs, jobs = jobs, pgs = pgs, curr_pg = pg, locations = locations, companies = companies, categories = categories, user = userDetail)
  

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
      application_id = cur.fetchone()[0]
      print(application_id)
      print(type(application_id))
      if application_id == None:
        application_id = 0
      application_id += 1
      cur.execute("insert into applications values(%(a)s, %(j)s, %(u)s, 0)", {'a': application_id, 'u': userid, 'j': jobid})
      conn.commit()
    return redirect('/user_{0}/0'.format(userid))
  else:
    return redirect('/login')


@app.route('/applications_<cmpid>_<jobid>')
def applications(cmpid, jobid):
  if not session.get('companyid'):
    return redirect('/login')
  if int(session.get('companyid')) != int(cmpid):
    return redirect('/login')

  conn = get_db_connection()
  cur = conn.cursor()
  
  cur.execute("""SELECT application_id, firstname, lastname, age, gender, education, email, contact, status, user_id FROM 
  (user_details NATURAL JOIN (SELECT * FROM applications WHERE  job_id = %(j_id)s) b) a ORDER BY application_id""", {"j_id": jobid })
  applicants = cur.fetchall()

  cur.execute("""SELECT * FROM experiences WHERE user_id IN 
  (SELECT user_id FROM applications WHERE job_id = %(j_id)s )""", {"j_id": jobid })
  exp = cur.fetchall()
  experiences = {}
  for e in exp:
    if e[5] in experiences:
      experiences[e[5]].append(e)
    else:
      experiences[e[5]] = []
      experiences[e[5]].append(e)
  #print(experiences)
  return render_template('applications.html', applicants=applicants, experiences=experiences, cmpid=cmpid, jobid = jobid)


def check_contact(contact):
  if len(contact) != 10:
    return False
  for c in contact:
    if c < '0' or c > '9':
      return False
  return True

@app.route('/user_profile_<int:userid>',methods=['POST', 'GET'])
def user_profile(userid):
  if not session.get('userid'):
    return redirect('/login')
  if session.get('userid') != userid:
    return redirect('/login')

  print("==========================")
  print(request.form)
  print("==========================")
  conn = get_db_connection()
  cur = conn.cursor()
  if request.method == "POST":
    if int(request.form['key']) == 1:
      fname = request.form['fname']
      lname = request.form['lname']
      age = request.form['age']
      gender = request.form['gender']
      eth = request.form['eth']
      address = request.form['address']
      mobile = request.form['mobile']
      education = request.form['education']
      state = request.form['state']
      if(not check_contact(mobile)):
        flash("Invalid contact number")
        cur.execute("select * from experiences where user_id = %(userid)s", {'userid': userid})
        experiences = cur.fetchall()
        cur.execute("select * from user_details where user_id = %(userid)s", {'userid': userid})
        userDetail = cur.fetchone()
        user_detail = UserDetails(userDetail[0], userDetail[1], userDetail[2], userDetail[3], userDetail[4], userDetail[5], userDetail[6], userDetail[7], userDetail[8], userDetail[9], userDetail[10])
        return render_template('user_profile.html', user_detail=user_detail, experiences=experiences)
        

      cur.execute("UPDATE user_details SET firstname = %(fname)s, lastname = %(lname)s, age = %(age)s, gender = %(gender)s, ethnicity = %(eth)s, address = %(address)s, state = %(state)s, contact = %(mobile)s, Education = %(education)s WHERE user_id = %(userid)s", {'userid':userid,  'fname': str(fname), 'lname': str(lname),'age': age, 'gender': str(gender), 'eth': str(eth),'address': str(address), 'state': str(state), 'mobile': str(mobile), 'education': str(education)})
      conn.commit()
      # print("UPDATE user_details SET firstname = %(fname)s, lastname = %(lname)s, age = %(age)s, gender = %(gender)s, ethnicity = %(eth)s, address = %(address)s, state = %(state)s, email = %(email)s, contact = %(mobile)s, Education = %(education)s WHERE user_id = %(userid)s", {'userid': str(user_id[0]), 'fname': str(fname), 'lname': str(lname),'age': str(age), 'gender': str(gender), 'eth': str(eth),'address': str(address), 'state': str(state), 'email': str(email), 'mobile': str(mobile), 'education': str(education)})
      flash("User profile updated successfully.", category = 'success')
    else:
      cur.execute("select max(exp_id) from experiences")
      exp_id = cur.fetchone()[0] + 1
      company = request.form['company']
      start = int(request.form['start'])
      end = int(request.form['end'])
      role = request.form['exp']
      cur.execute("INSERT INTO experiences VALUES(%(exp_id)s, %(company)s, %(start)s, %(end)s, %(role)s, %(userid)s)", {'exp_id': exp_id, 'userid': userid, 'start': start, 'end': end, 'role': role, 'company': company})
      conn.commit()


  cur.execute("select * from experiences where user_id = %(userid)s", {'userid': userid})
  experiences = cur.fetchall()

  cur.execute("select * from user_details where user_id = %(userid)s", {'userid': userid})
  userDetail = cur.fetchone()
  user_detail = UserDetails(userDetail[0], userDetail[1], userDetail[2], userDetail[3], userDetail[4], userDetail[5], userDetail[6], userDetail[7], userDetail[8], userDetail[9], userDetail[10])
  return render_template('user_profile.html', user_detail=user_detail, experiences=experiences)

@app.route('/company_profile_<int:cmpid>',methods=['POST', 'GET'])
def company_profile(cmpid):
  if not session.get('companyid'):
    return redirect('/login')
  if int(session.get('companyid')) != int(cmpid):
    return redirect('/login')
  print("==========================")
  print(request.form)
  print("==========================")
  conn = get_db_connection()
  cur = conn.cursor()
  if request.method == "POST":
    if int(request.form['key']) == 1:
      cname = request.form['cname']
      about = request.form['about']
      depts = request.form['depts']
      location = request.form['location']
      awds = request.form['awds']
      contact = request.form['contact']
      website = request.form['website']
      if(not check_contact(contact)):
        flash("Invalid contact number")
        cur.execute("select * from company_details where company_id = %(compid)s", {'compid': cmpid})
        compDetail = cur.fetchone()
        company_detail = companyDetails(compDetail[0], compDetail[1], compDetail[2], compDetail[3], compDetail[4], compDetail[5], compDetail[6], compDetail[7], compDetail[8], compDetail[9])
        return render_template('company_profile_new.html', company_detail=company_detail)
        
      cur.execute("UPDATE company_details SET company_name = %(cname)s, about_us = %(abt)s, department = %(dep)s, location = %(loc)s, awards = %(awd)s, contact = %(cont)s, website = %(webs)s WHERE company_id = %(compid)s", {'compid':cmpid,  'cname': str(cname), 'abt': str(about),'dep': str(depts), 'loc': str(location), 'awd': str(awds),'cont': str(contact), 'webs': str(website)})
      conn.commit()
      flash("Company profile updated successfully.", category = 'success')


  cur.execute("select * from company_details where company_id = %(compid)s", {'compid': cmpid})
  compDetail = cur.fetchone()
  company_detail = companyDetails(compDetail[0], compDetail[1], compDetail[2], compDetail[3], compDetail[4], compDetail[5], compDetail[6], compDetail[7], compDetail[8], compDetail[9])
  return render_template('company_profile_new.html', company_detail=company_detail)
  

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
                    FROM job_details as jobs
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
    status_map = {'1': "OPEN", '0': "CLOSED"}
    for job in jobs:
      job_details.append(JobDetail(job[0], company[1], job[2], job[3], job[4], job[5], job[6], job[7], job[8], job[9], company[2], company[7], company[8], job_status=status_map[job[10]]))
    return render_template('companyPage.html', jobs = job_details, company_detail = company_detail)
  
  if request.method == "POST":
    print("==========================")
    print("Handling POST request")
    print("==========================")
    # TODO Needs to be changed
    return redirect('/user/0')


@app.route('/delete_job_<int:cmpid>/<int:jobid>')
def delete_job(cmpid, jobid):
  if not session.get('companyid'):
    return redirect('/login')
  if int(session.get('companyid')) != int(cmpid):
    return redirect('/login')
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute("DELETE FROM job_details WHERE job_id = %(o)s", {"o": jobid})
  conn.commit()
  return redirect('/company_' + str(cmpid))

@app.route('/update_job_status_<int:cmpid>_<int:jobid>_<int:newstatus>')
def update_job_status(cmpid, jobid, newstatus):
  if not session.get('companyid'):
    return redirect('/login')
  if int(session.get('companyid')) != int(cmpid):
    return redirect('/login')
  conn = get_db_connection()
  cur = conn.cursor()
  if newstatus == 0:
    cur.execute("UPDATE job_details SET status = '0' WHERE job_id = %(o2)s", {"o2": jobid})
  else:
    cur.execute("UPDATE job_details SET status = '1' WHERE job_id = %(o2)s", {"o2": jobid})
  conn.commit()
  return redirect('/company_' + str(cmpid))

@app.route('/update_appl_status_<int:cmpid>_<int:jobid>_<int:appid>_<int:newstatus>')
def update_appl_status(cmpid, jobid, appid, newstatus):
    if not session.get('companyid'):
      return redirect('/login')
    if int(session.get('companyid')) != int(cmpid):
      return redirect('/login')
    conn = get_db_connection()
    cur = conn.cursor()
    newstatus = int(newstatus)
    if newstatus == 1:
      print('here1')
      cur.execute("UPDATE applications SET status = 1 WHERE application_id = %(o2)s", {"o2": appid})
    elif newstatus == 2:
      print('here1')
      cur.execute("UPDATE applications SET status = 2 WHERE application_id = %(o2)s", {"o2": appid})
    conn.commit()
    return redirect('/applications_' + str(cmpid) + '_' + str(jobid))

@app.route('/company_profile')
def getcompany_profile():
  return render_template('company_profile.html')

@app.route('/postjob_<int:cmpid>', methods=["GET", "POST"])
def createjob(cmpid):
  if not session.get('companyid'):
    return redirect('/login')
  if int(session.get('companyid')) != int(cmpid):
    return redirect('/login')
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute("select company_name, email from company_details where company_id = %(o)s", {"o": cmpid})
  company = cur.fetchone()
  cmp_name = company[0]
  cmp_email = company[1]
  if request.method == "GET":
    return render_template('postJob.html', companyid=cmpid, cmp_name=cmp_name, cmp_email=cmp_email)
  if request.method == "POST":
    cur.execute("select max(job_id) from job_details")
    job_id = cur.fetchone()[0]+1
    company_id = cmpid
    title = request.form['title']
    description = request.form['description']
    job_type = request.form['job_type']
    prerequisites = request.form['prerequisites']
    skills = request.form['skills']
    pay_rate = request.form['pay_rate']
    no_positions = request.form['no_positions']
    experience_required = request.form['experience_required']

    cur.execute("INSERT INTO job_details (job_id, company_id, title, description, job_type, prerequisites, skills, pay_rate, no_positions, experience_required, status) VALUES (%(o1)s, %(o2)s, %(o3)s, %(o4)s, %(o5)s, %(o6)s, %(o7)s, %(o8)s, %(o9)s, %(o10)s, '1')", {"o1": job_id, "o2": company_id, "o3": title, "o4": description, "o5": job_type, "o6": prerequisites, "o7": skills, "o8": pay_rate, "o9": no_positions, "o10": experience_required})
    conn.commit()
    return redirect('/company_' + str(cmpid))
  return render_template('postJob.html', companyid=cmpid, cmp_name=cmp_name, cmp_email=cmp_email)




if __name__ == '__main__':
  app.run(debug=True, port=5020)