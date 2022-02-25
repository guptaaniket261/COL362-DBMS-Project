import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import csv
import os
# for dirname, _, filenames in os.walk('/kaggle/input'):
#     for filename in filenames:
#         print(os.path.join(dirname, filename))

def is_in_english(quote):
    c = ord(quote[0])
    a = ord('a')
    if (c-a < 0) or (c-a >25):
        return False
    return True

data = pd.read_csv('/kaggle/input/jobs-on-naukricom/naukri_com-job_sample.csv')
data2 = pd.read_csv('/kaggle/input/naukri/2019_free_title_data.csv')
df = pd.DataFrame(data) 
df2 = pd.DataFrame(data2)
companies = df.iloc[:]['company']
experiences = df.iloc[:]['experience']
titles = df2.iloc[:]['title']
np.random.shuffle(companies)
np.random.shuffle(experiences)
np.random.shuffle(titles)
c = list(set(companies))
c = list(map(str,c))
banned = ['hiring','for','/','nan']
companies=[]
for comp in c:
    if len(companies)==2000:
        break
    if any([x in comp for x in banned]):
        continue
    else:
        companies.append(comp)
exps=[]
for exp in experiences:
    if len(exps)==2000:
        break
    duration = str(exp).split()
    if 'Not' in duration:
        continue
    else:
        exps.append(exp)
roles = []
for role in titles:
    if(len(roles)==2000):
        break
    if is_in_english(str(role)):
        roles.append(str(role))

# print(len(companies))
# print(len(exps))
# print(titles)
fields = ['exp_id','company','start_year','years','role']
rows = []
for i in range(2000):
    row = []
    row.append(i+1)
    row.append(companies[i])
    duration = str(exps[i]).split()
    row.append(2000+int(duration[0]))
    row.append(2000+int(duration[2]))
    row.append(roles[i])
    rows.append(row)
    print(row)
    
with open('experiences', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
      
    write.writerow(fields)
    write.writerows(rows)

