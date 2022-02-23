from dataclasses import fields
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import csv
import os
import random as r


def gen_contact():
    ph_no = []    
    ph_no.append(str(r.randint(6, 9)))
    for i in range(1, 10):
        ph_no.append(str(r.randint(0, 9)))
    contact = "".join(ph_no)
    return contact  

data = pd.read_csv('user.csv')
df = pd.DataFrame(data) 
first_names = df.iloc[:]['fname']
last_names = df.iloc[:]['lname']
genders = df.iloc[:]['gender']
eths = df.iloc[:]['eth']
emails = list(map(lambda x: x+"@gmail.com" ,first_names))
ages = list(np.random.randint(low = 20, high = 75, size = 2000))

data2 = pd.read_csv('addresses.csv')
df2 = pd.DataFrame(data2) 
addresses = df2.iloc[:]['Address']
fields = ["userId","firstname","lastname","age","gender","ethnicity","address","pastExperience","email","contact"]
rows = []
for i in range(2000):
    row = []
    row.append(i+1)
    row.append(first_names[i])
    row.append(last_names[i])
    row.append(ages[i])
    row.append(genders[i])
    row.append(eths[i])
    row.append(addresses[i%len(addresses)])
    exp = []
    exp.append(r.randint(1,2000))
    exp.append(r.randint(1,2000))
    row.append(exp)
    row.append(emails[i])
    row.append(gen_contact())
    rows.append(row)
    print(row)

with open('userDetails', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
      
    write.writerow(fields)
    write.writerows(rows)
    



 
