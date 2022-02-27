from dataclasses import fields
from operator import index
from matplotlib import use
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import csv
import os
import random as r
import copy

exp_data = pd.read_csv('experiences.csv')
exp_df = pd.DataFrame(exp_data)
user_data = pd.read_csv('userDetails.csv')
user_df = pd.DataFrame(user_data)
#print(exp_data)
#print(user_data)

newFields = ["userId","firstname","lastname","age","gender","ethnicity","address","state","email","contact","Education"]

exps = user_df.iloc[:]['pastExperience']

arr = []
for i in range(len(exps)):
    s = exps[i][1:len(exps[i]) - 1]
    s_arr = s.split(',')
    for j in range(len(s_arr)):
        s_arr[j] = s_arr[j].strip()
    num_arr = [int(s_arr[0]), int(s_arr[1])]
    arr.append([i+1, num_arr[0]])
    arr.append([i+1, num_arr[1]])

newdataset = []
count = 1
for idx, row in exp_data.iterrows():
    
    for k in range(len(arr)):
        if arr[k][1] == int(row['exp_id']):
            rr = []
            rr.append(count)
            count += 1
            rr.append(row["company"])
            rr.append(row["start_year"])
            rr.append(row["years"])
            rr.append(row["role"])
            rr.append(arr[k][0])
            newdataset.append(rr)

fields = ['exp_id','company','start_year','years','role','user_id']

with open('experiencesNew', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(fields)

    write.writerows(newdataset)
    

'''
del user_df['pastExperience']
user_df.to_csv('new.csv', index=False)
'''