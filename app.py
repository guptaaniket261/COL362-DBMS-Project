import os
import psycopg2
from flask import Blueprint, Flask, render_template, redirect, request, flash
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
  return redirect('/login')


@app.route('/login', methods=["GET", "POST"])
def login():
  print(request.method)
  if request.method == "POST":
    email = request.form['email']
    password = request.form['password']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM login_details WHERE login_id = %s AND password = %s", (email, password))
    conn.commit()
    user = cur.fetchone()
    print(user)
    conn.close()
    if user:
      return redirect("http://127.0.0.1:5000/user/'{0}'".format(user))
    else:
      return render_template('loginPage.html')
  return render_template('loginPage.html')
  

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
      flash('User already exists',category='error')
      return redirect('/user_register')
    else:
      if user_type == "applicant":
        cur.execute("INSERT INTO user_details VALUES (DEFAULT, NULL, NULL,NULL,NULL,NULL,NULL,NULL,%(o)s, NULL, NULL)", {'o': str(email)})
        conn.commit()
        cur.execute("select user_id from user_details where email = %s", (email))
        user_id = cur.fetchone()
        print("=====================")
        print(user_id)
        print("=====================")
        
        cur.execute("INSERT INTO login_details VALUES (DEFAULT, %(email)s, %(password)s, 'applicant', %(userid)s, NULL)", {'email': str(email), 'password': str(password), 'userid': str(user_id[0])})
        conn.commit()
        # cur.execute("INSERT INTO login_details VALUES (DEFAULT, %s, %s, %s, %s, NULL)", (email, password, "user", user[]))
        # conn.commit()
        # flash('User registered successfully',category='success')
    return redirect('/login')
  return render_template('user_register.html')


@app.route('/user')
def user():
  # if(userDetails.user_id == -1):
  #   return redirect('/login')
  return redirect('/user/0')

@app.route('/user/<offset>', methods=["GET", "POST"])
def userpage(offset):
  # print("==========================")
  # print(USER_DETAILS.firstname)
  # print("==========================")
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



@app.route('/applications/<jobid>')
def applications(jobid):
  # return render_template('loginPage.html')
  conn = get_db_connection()
  cur = conn.cursor()
  # TODO Query to be changed
  cur.execute("SELECT application_id, firstname, lastname, age, gender, education, email, contact, status FROM user_details NATURAL JOIN (SELECT * FROM applications WHERE  job_id = %(j_id)s))", {"j_id": jobid })
  applicants = cur.fetchall()

  return render_template('applications.html', applicants=applicants)


@app.route('/user_profile',methods=['POST', 'GET'])
def profile():
    if request.method == "POST":
      fname = request.form['fname']
      lname = request.form['lname']
      age = request.form['age']
      gender = request.form['gender']
      eth = request.form['eth']
      address = request.form['address']
      mobile = request.form['mobile']
      email = request.form['email']
      education = request.form['education']
      country = request.form['country']
      state = request.form['state']
      print(fname)
      conn = get_db_connection()
      cur = conn.cursor()
      cur.execute("select user_id from user_details where email = %(email)s", {'email': str(email)})
      user_id = cur.fetchone()
      if user_id:
        print(user_id)
        cur.execute("UPDATE user_details SET firstname = %(fname)s, lastname = %(lname)s, age = %(age)s, gender = %(gender)s, ethnicity = %(eth)s, address = %(address)s, state = %(state)s, email = %(email)s, contact = %(mobile)s, Education = %(education)s WHERE user_id = %(userid)s", {'userid': str(user_id[0]), 'fname': str(fname), 'lname': str(lname),'age': str(age), 'gender': str(gender), 'eth': str(eth),'address': str(address), 'state': str(state), 'email': str(email), 'mobile': str(mobile), 'education': str(education)})
        conn.commit()
        print("UPDATE user_details SET firstname = %(fname)s, lastname = %(lname)s, age = %(age)s, gender = %(gender)s, ethnicity = %(eth)s, address = %(address)s, state = %(state)s, email = %(email)s, contact = %(mobile)s, Education = %(education)s WHERE user_id = %(userid)s", {'userid': str(user_id[0]), 'fname': str(fname), 'lname': str(lname),'age': str(age), 'gender': str(gender), 'eth': str(eth),'address': str(address), 'state': str(state), 'email': str(email), 'mobile': str(mobile), 'education': str(education)})
        flash("User profile updated successfully.")

    return render_template('user_profile.html')



@app.route('/company_profile')
def getcompany_profile():
  return render_template('company_profile.html')


@app.route('/postjob')
def createjob():
  return render_template('postJob.html')


@app.route('/company/<cmpid>', methods=["GET", "POST"])
def cmppage(cmpid):
  print(request.form)
  if request.method == "GET":
    conn = get_db_connection()
    cur = conn.cursor()
    if cmpid.isnumeric():
      cmpid = int(cmpid)
    else:
      print("Invalid companyid")
    cur.execute("SELECT * FROM job_details WHERE company_id = %(c)s", {"c": cmpid})
    jobs = cur.fetchall()
    print(jobs)

    return render_template('companyPage.html', jobs = jobs)
  
  if request.method == "POST":
    print("==========================")
    print("Handling POST request")
    print("==========================")
    # TODO Needs to be changed
    return redirect('/user/0')

if __name__ == '__main__':
  app.run(debug=True)