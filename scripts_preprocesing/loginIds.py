from dataclasses import fields
from operator import index
from matplotlib import use
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import csv
import os
import random as r
import copy


user_data = pd.read_csv('userDetailsLatest.csv')
df = pd.DataFrame(user_data)

company_data = pd.read_csv('company_details_latest.csv')
company_df = pd.DataFrame(company_data)

fields = ["pid", "login_id", "password", "userorcompany", "user_id", "company_id"]


newDataset = []
cou = 1
for idx, row in user_data.iterrows():
  temp = []
  temp.append(cou)
  temp.append(row['email'])
  temp.append(''.join(str(r.randint(0, 9)) for i in range(6)))
  temp.append('user')
  temp.append(row['userId'])
  temp.append("null")
  newDataset.append(temp)
  # temp["pid"] = cou
  # temp["login_id"] = row["email"]
  # temp["password"] = ''.join(str(r.randint(0, 9)) for i in range(6))
  # temp["userorcompany"] = "user"
  # temp["user_id"] = row["userId"]
  # temp["company_id"] = "null"
  # newDataset.append(temp)
  cou += 1

for idx, row in company_data.iterrows():
  temp = []
  temp.append(cou)
  temp.append(row['email'])
  temp.append(''.join(str(r.randint(0, 9)) for i in range(6)))
  temp.append('company')
  temp.append("null")
  temp.append(row['company_id'])
  newDataset.append(temp)

  # temp["pid"] = cou
  # temp["login_id"] = row["email"]
  # temp["password"] = ''.join(str(r.randint(0, 9)) for i in range(6))
  # temp["userorcompany"] = "company"
  # temp["user_id"] = "null"
  # temp["company_id"] = row["company_id"]
  # newDataset.append(temp)
  cou += 1

with open('login_details.csv', 'w', newline='', encoding='utf-8' ) as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(fields)

    write.writerows(newDataset)



