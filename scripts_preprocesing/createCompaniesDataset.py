import numpy as np
import pandas as pd
import csv
import os
import random
# for dirname, _, filenames in os.walk('/kaggle/input'):
#     for filename in filenames:
#         print(os.path.join(dirname, filename))

# read csv file using pandas
data = pd.read_csv(r'C:\Users\gupta\Sem6\COL362_DBMS\project\COL362-DBMS-Project\tables\jobDataset.csv')
df = pd.DataFrame(data)


# columns for Comapny details
company_name = list(df.iloc[:]['company'])
print(type(company_name))
print(company_name[5])
joblocation = list(df.iloc[:]['joblocation_address'])
departments = list(df.iloc[:]['industry'])
company_rows = []
banned = ['hiring','for','/','nan']
company_set = set()
count = 0
company_to_id = {}
for i in range(len(company_name)):
  if any([x in str(company_name[i]) for x in banned]):
    continue
  else:
    comp = company_name[i]
    if comp in company_set:
      continue
    count += 1
    company_set.add(comp)
    company_to_id[comp] = count
    location = joblocation[i]
    department = departments[i]
    about_us = "we are {0}".format(comp)
    rating = random.randint(1,5)
    awards = "Best Company in field of {0}".format(department)
    contact = str(random.randint(1111111111,9999999999))
    temp = comp.strip().split()
    tt = ""
    for t in temp:
      tt += t
    email = "{0}.gmail.com".format(tt)
    website = "{0}.com".format(tt)
    row = [count, comp,location,department,about_us,rating,awards,contact,email,website]
    company_rows.append(row)

with open(r'C:\Users\gupta\Sem6\COL362_DBMS\project\COL362-DBMS-Project\tables\company_details.csv', 'w', newline='') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(['company_id','company_name','location','department','about_us','rating','awards','contact','email','website'])
  writer.writerows(company_rows)



# columns for jobs
title = df.iloc[:]['jobtitle']
description = df.iloc[:]['jobdescription']
jobType = ['part-time','full-time','internship','contract', 'work-from-home']
prereq = df.iloc[:]['education']
role = df.iloc[:]['skills']
pay = df.iloc[:]['payrate']
noPositions = df.iloc[:]['numberofpositions']
experienceRequired = df.iloc[:]['experience']
status = [0, 1]
job_rows = []


count = 0
for i in range(len(title)):
  if(company_name[i] in company_set):
    row = []
    count += 1
    row.append(count)
    row.append(company_to_id[company_name[i]])
    row.append(title[i])
    row.append(description[i])
    row.append(jobType[random.randint(0,4)])
    row.append(prereq[i])
    row.append(role[i])
    row.append(pay[i])
    row.append(noPositions[i])
    row.append(experienceRequired[i])
    row.append(status[random.randint(0,1)])
    job_rows.append(row)

with open(r'C:\Users\gupta\Sem6\COL362_DBMS\project\COL362-DBMS-Project\tables\job_details.csv', 'w', newline='', encoding="utf-8") as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(['job_id','company_id','title','description','job_type','prerequisites','skills','pay_rate','no_positions','experience_required','status'])
  writer.writerows(job_rows)






