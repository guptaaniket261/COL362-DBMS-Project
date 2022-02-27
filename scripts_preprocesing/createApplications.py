from dataclasses import fields
from email.mime import application
from itertools import count
from operator import index
from importlib_metadata import files
from matplotlib import use
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import csv
import os
import random as r
import copy
import re


skills = [
 "beauty",
 "fitness",
 "spa",
 "product",
 "hardware",
 "teach",
 "software",
 "Software",
 "Design",
 "design",
 "medical",
 "financ",
 "architect",
 "TV",
 "Executive",
 "Mobile",
 "Supply",
 "Packag",
 "Accounts",
 "Fashion",
 "Manage",
 "telecom",
 "market",
 "analys",
 "Sales",
 "legal",
 "Hotel",
 "Defence",
 "Export",
 "network",
 "Travel",
 "HR",
 "Journal",
 "Strategy",
 "techno",
 "engineer",
  "business"
]


exp_data = pd.read_csv('experiencesNew.csv')
exp_df = pd.DataFrame(exp_data)

dic = {}

for idx, row in exp_data.iterrows():
    for s in skills:
        if re.search(s, row['role'], re.IGNORECASE) or re.search(s, row['company'], re.IGNORECASE):
            if s in dic:
                dic[s].append(row['user_id'])
            else :
                dic[s] = [row["user_id"]]

dic2 = {}

job_data = pd.read_csv('job_details.csv')
job_df = pd.DataFrame(job_data)
for idx, row in job_data.iterrows():
    for x in skills:
        if pd.isna(row["skills"]): continue
        if re.search(x, row['skills'], re.IGNORECASE):
            if x in dic2:
                dic2[x].append(row['job_id'])
            else :
                dic2[x] = [row["job_id"]]
print(dic2)

count = 1
applications = []
for h in skills:
    if h not in dic or h not in dic2: continue
    users = dic[h]
    jobs = dic2[h]
    for u in users:
        for j in jobs:
            p = (1/len(users)) * (1/len(jobs))
            if(r.random() < 500 * p):
                row = []
                row.append(count)
                count+=1
                row.append(j)
                row.append(u)
                row.append(r.choice(range(3)))
                applications.append(row)

fields = ['application_id', 'job_id', 'user_id', 'status']
with open('applications.csv', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(fields)

    write.writerows(applications)


