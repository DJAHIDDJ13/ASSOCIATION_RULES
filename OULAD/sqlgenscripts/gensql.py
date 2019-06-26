# -*- coding:utf-8 -*-
import pandas as pd
import sys, os
from sqlutil import *

dataset_dir = '../'
last_update = 0

for fl in os.listdir(dataset_dir): # parse files in the dataset directory
    if not fl.endswith('.csv'): # ignore non-csv files
        continue

    table = fl[:-4] # remove csv extension
    print("Generating insert script for '{}'".format(table))

    # reading the data
    df = pd.read_csv(dataset_dir+fl).replace('?', '0') # read the csv file and replace ? with zeros
    
    # there is a special case where a columns name is 'date' which is a reserved word in sql
    df.rename(columns={u'date':table+u'_date'}, inplace=True)
    
    batchsize = 1000000
    n = (len(df)//batchsize)+1
    for batchno in range(n):
        with open('./INSERT_DATA_{}{}.sql'.format(table, '' if batchno == 0 else '_'+str(batchno)), 'w') as f:
            print('batch {}/{}'.format(batchno+1, n))
            print(batchno*batchsize, (batchno+1)*batchsize if batchno != n-1 else len(df))
            for i in range(batchno*batchsize, (batchno+1)*batchsize if batchno != n-1 else len(df)):
                # show the progress bar
                last_update = show_prog(i+1, len(df), last_update)

                # the data entry to be written to the output file
                entry = {}
                for col in df: 
                    entry[col] = df[col][i]
                
                # write the generated sql insert of the entry to the output file
                f.write(insert(table, **entry)+'\n')
            print # newline


# for the students table
with open('./INSERT_DATA_students.sql', 'w') as f:
    student_ids = []
    df = pd.read_csv(dataset_dir+'studentInfo.csv')
    for i in range(len(df)):
        s_id = df['id_student'][i]
        if s_id not in student_ids:
            f.write(insert('Students', **{'id_student': s_id})+'\n')
            student_ids.append(s_id)

