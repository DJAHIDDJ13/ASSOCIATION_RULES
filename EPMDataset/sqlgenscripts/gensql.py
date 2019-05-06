# -*- coding:utf-8 -*-
from sqlutil import *
import pandas as pd
import sys, os
import re

# recursive parsing of directory
def scrap_data(path):
    # scraping the sessions' data
    print("Scraping the emp data..")
    emps = pd.DataFrame(columns=['session_id', 'student_id', 'exercice', 'activity', 'start_time', 'end_time', 'idle_time', 'mouse_wheel', 'mouse_wheel_click', 'mouse_click_left', 'mouse_click_right', 'mouse_movement', 'keystroke'])
    for root, dirs, files in os.walk(path + '/Processes'):
        if root != path + '/Processes':
            for student in files:
                emps = emps.append(pd.read_csv(root+'/'+student, header=None, names=emps.columns))
    emps.replace(to_replace=r'\'\s+', value=r'\'', inplace=True)
    # scraping session presence log
    print('Scraping the presence log..')
    pres = pd.read_csv(path + '/logs.txt', sep='\t')
    presence = pd.DataFrame(columns=['student_id', 'session_id', 'present'])
    for i in range(len(pres)):
        for col in pres.columns:
            if col != 'Student Id':
                session_id = int(col.split()[1])
                student_id = pres.iloc[i]['Student Id']
                presence = presence.append({'student_id': student_id,
                                         'session_id': session_id,
                                         'present': 'true' if pres.iloc[i][col] else 'false'},
                                        ignore_index=True)

    # scraping the grades
    print('Scraping the intermediate grades..')
    # intermediate grades
    inter_raw = pd.read_excel(path + '/intermediate_grades.xlsx')
    inter = pd.DataFrame(columns=['student_id', 'session_id', 'grade'])
    for i in range(len(inter_raw)):
        for col in inter_raw.columns:
            if col != 'Student Id':
                session_id = int(col.split()[1])
                student_id = inter_raw.iloc[i]['Student Id']
                inter = inter.append({'student_id': student_id,
                                      'session_id': session_id,
                                      'grade': inter_raw.iloc[i][col]},
                                      ignore_index=True)

    # final grades
    print('Scraping the final grades..')
    ## regex to rename ES #.# (# points) to # # #  and  Student ID to student_id
    norm = lambda c: re.sub(r'ES (\d+)\.(\d+) ?\n\((\d+) points\)', r'\1 \2 \3', re.sub(r'Student ID', r'student_id', c))

    final1 = pd.read_excel(path + '/final_grades.xlsx', 'Exam (First time)').drop('TOTAL\n(100 points)', axis=1)
    final1.rename(columns=norm, inplace=True)
    final1['passage_no'] = 1

    final2 = pd.read_excel(path + '/final_grades.xlsx', 'Exam (Second time)').drop('TOTAL\n(100 points)', axis=1)
    final2.rename(columns=norm, inplace=True)
    final2['passage_no'] = 2

    final12 = pd.concat([final1, final2])
    final = pd.DataFrame(columns=['student_id', 'session_id', 'question_no', 'max_grade', 'grade'  , 'passage_no'])

    cols = final12.columns
    for i in range(len(final12)):
        for col in cols:
            if col != 'student_id' and col != 'passage_no':
                session_id, question_id, max_grade = map(int, col.split())
                student_id = int(final12.iloc[i]['student_id'])
                final = final.append({'student_id': student_id,
                                      'session_id': session_id,
                                      'question_no': question_id,
                                      'max_grade': max_grade,
                                      'grade': final12.iloc[i][col],
                                      'passage_no': final12.iloc[i]['passage_no']},
                                      ignore_index=True)

    return emps, presence, inter, final

def write_dataframe(f, tablename, df):
    last_update = 0

    print(tablename+':')
    ln = len(df)
    for i in range(ln):
        last_update = show_prog(i+1, ln, last_update)
        d = {}
        for col in df.columns:
            val = df.iloc[i][col]
            d[col] = str(val) if col in floats else (str(int(val)) if col in ints else "'" + str(val) + "'")
        f.write(insert(tablename, **d)+'\n')

# opening the output file
f = open('./INSERT_DATA.sql', 'w')
print('Output file {} opened'.format('../INSERT_DATA.sql'))

# the table names
ints = ['student_id', 'session_id', 'question_no', 'passage_no', 'idle_time', 'mouse_wheel', 'mouse_wheel_click', 'mouse_click_left', 'mouse_click_right', 'mouse_movement', 'keystroke']
floats = ['grade', 'max_grade']
emp, presence, inter, final = scrap_data('../Data')


no_students = 115
no_sess = 6

for i in range(no_students):
    f.write(insert('Students', **{'student_id':i+1})+'\n')
for i in range(no_sess):
    f.write(insert('Sessions', **{'session_id':i+1})+'\n')

write_dataframe(f, 'FinalGrade', final)
write_dataframe(f, 'InterGrade', inter)
write_dataframe(f, 'Presence', presence)
write_dataframe(f, 'Epm', emp)

# closing the output file
f.close()
print('Output file {} closed'.format('../INSERT_DATA.sql'))
