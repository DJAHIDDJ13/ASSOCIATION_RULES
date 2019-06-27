import pandas as pd
import numpy as np
import mlxtend as ml
import psycopg2 as ps
import sys, pprint
from mlxtend.frequent_patterns import association_rules
from mlxtend.frequent_patterns import apriori

def main():
        conn_string = """
                        host='10.77.21.121'
                        dbname='oulad'
                        user='postgres'
                        password='123456'
                      """
	# get a connection, if a connect cannot be made an exception will be raised here
        conn = ps.connect(conn_string)
 
	# conn.cursor will return a cursor object, you can use this cursor to perform queries
        cursor = conn.cursor()

        cursor.execute("""
        select * from
        (select
        final_result, id_site
        from
        studentInfo right join studentVle
        on studentInfo.id_student = studentVle.id_student
        ) as info_vle
        left join
        vle
        on vle.id_site = info_vle.id_site
        ;
        """)
        # create the dataframe
        records = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

        # get dummies
        records = pd.get_dummies(records)
        
        frequent_itemsets = apriori(records, min_support=0.001, use_colnames=True)
        assoc_rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)

        print('\n****THE FREQUENT DATASETS:****')
        print(frequent_itemsets)
        print('\n*****THE ASSOCIATION RULES:****')
        
        for i in range(len(assoc_rules)):
                assoc_rule = assoc_rules.iloc[i]
                print(f"{assoc_rule['antecedents']} -> {assoc_rule['consequents']} conf:{round(assoc_rule['confidence']*100,2)}%, supp:{round(assoc_rule['support']*100, 2)}%")
        


if __name__ == "__main__":
	main()
