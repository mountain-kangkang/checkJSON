import os
from iteration_utilities import duplicates
import csv

def listDups(listNums):
  return list(duplicates(listNums))

result = os.walk('E:\\2D\\87 로드마크\\XIILAB\\')

all_root_list = []
file_name_list = []
csv_list = []
fields = ['root', 'file name']

for root, dirs, files in result:
    for f in files:
        if '.json' in f:
            all_root_list.append(root)
            file_name_list.append(f)

dup_file_list = listDups(file_name_list)

for i in range(len(all_root_list)):
    if file_name_list[i] in dup_file_list:
        tmp_list = [all_root_list[i], file_name_list[i]]
        csv_list.append(tmp_list)

with open('test1.csv', 'w', newline='') as f:
    write = csv.writer(f)
    write.writerow(fields) 
    write.writerows(csv_list)

print('--------Done---------')