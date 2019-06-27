import pandas as pd
import numpy as np
import mlxtend as ml
import psycopg2 as ps
import sys, pprint
from mlxtend.frequent_patterns import association_rules, apriori
from datetime import datetime
from pprint import pprint

def main():
        conn_string = """
                        host='172.20.10.3'
                        dbname='epm'
                        user='postgres'
                        password='123456'
                      """
	# get a connection, if a connect cannot be made an exception will be raised here
        conn = ps.connect(conn_string)
 
	# conn.cursor will return a cursor object, you can use this cursor to perform queries
        cursor = conn.cursor()
        
        # joining the tables
        cursor.execute("""
            select start_time, end_time, epm.student_id, epm.session_id,i_grade, question_no, max_grade, grade, passage_no,exercice, activity, mouse_wheel, mouse_wheel_click, mouse_click_left, mouse_click_right, mouse_movement, keystroke
            from
                (select finalgrade.student_id,finalgrade.session_id,intergrade.grade as i_grade, question_no, max_grade, finalgrade.grade, passage_no
                    from intergrade right join finalgrade
                    on intergrade.student_id = finalgrade.student_id and intergrade.session_id = finalgrade.session_id
                ) as grades
                right join epm
                on grades.student_id = epm.student_id and grades.session_id = epm.session_id
                ;
        """)
        # create the dataframe
        records = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

        # remove _Es_#_# from the end and transform to lowercase
        records['activity'] = records['activity'].str.lower().replace(regex=True,to_replace=r'_es(_\d_\d)?',value=r'')
        #records['exercice'] = records['activity'].str.lower().replace(regex=True,to_replace=r'_es(_\d_\d)?',value=r'')

        # calculate the final grade (finalgrade / max_final + intermediategrade / max_inter) / 2
        max_sess = [0,6,4,5,4,4] # the max for each session
        records['grade'] = records['grade'] / (2*records['max_grade']) + records['i_grade'] / (2*records['session_id'].map(lambda x: max_sess[int(x)-1]))
        records.fillna(0, inplace=True)

        # only get the grade and the activity
        # records = records.loc[:,['grade', 'activity']]

        # calculate the duration
        fmt = '%Y-%m-%d %H:%M:%S'
        records['duration'] = (records['end_time'] - records['start_time'])/np.timedelta64(1,'s')

        # drop the rest 
        records = records.drop(columns=['start_time', 'end_time', 'i_grade', 'question_no', 'max_grade','student_id', 'session_id', 'passage_no'])
        
        ## discretisation
        # unequal bins
        def jitter(a_series, noise_reduction=1000000):
            return (np.random.random(len(a_series))*a_series.std()/noise_reduction)-(a_series.std()/(2*noise_reduction))
        for col in records.columns:
                if col not in ['exercice', 'activity']: # todo: except strings instead of specific attributes
                        try:
                                records[col] = pd.qcut(records[col], 4) # discretecize the grade column
                        except:
                                p = sum(records[col]==0)/len(records)
                                q = (1-p) / 3
                                records[col] = pd.qcut(records[col]+jitter(records[col]), [p,p+q,p+2*q,p+3*q]) # discretecize the grade column
        ## uncomment to save the result in csv files
        #records.to_csv('Epm_records.csv') # uncomment this line 
  
        print(records.columns)
        # get the original attribute names
        confmat = {row: {col: [] for col in records.columns} for row in records.columns}

        # get the dummified version of the attributes
        records = pd.get_dummies(records, prefix_sep =';')
        #records.to_csv('Epm_records_dummy.csv') # and this
                                
        print(records.columns)        
        
        print('\n****THE FREQUENT DATASETS:****')
        frequent_itemsets = apriori(records, min_support=0.005, use_colnames=True)
        print(frequent_itemsets)

        print('\n*****THE ASSOCIATION RULES:****')
        assoc_rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.01)
        assoc_rules = sorted([assoc_rules.iloc[i] for i in range(len(assoc_rules))], key=lambda x: x['confidence'])
        for assoc_rule in assoc_rules:
                if len(assoc_rule['antecedents']) == 1 and len(assoc_rule['consequents']) == 1:
                        ante = list(assoc_rule['antecedents'])[0]
                        cons = list(assoc_rule['consequents'])[0]
                        print(f"{ante} -> {cons} "+
                              f"conf:{round(assoc_rule['confidence']*100,2)}%, "+
                              f" supp:{round(assoc_rule['support']*100, 2)}%")
                        orig_ante, orig_ante_dum = ante.split(';')
                        orig_cons, orig_cons_dum = cons.split(';')
                        
                        confmat[orig_ante][orig_cons].append([orig_ante_dum, orig_cons_dum, round(assoc_rule['confidence']*100,2), round(assoc_rule['support']*100, 2)])
        ### confmat format ###
        # To access a member of confmat, get confmat[<attr1>][<attr2>] which is an array
        # of arrays of size 4 each one of these sub-arrays are formed this way
        # [<interval_of_antecedent>, <interval_of_consequent>, <confidence>, <support>]

        pprint(confmat)
if __name__ == "__main__":
	main()
