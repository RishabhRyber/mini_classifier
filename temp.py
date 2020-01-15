import pandas as pd
import mysql.connector
import numpy as np
from sklearn import tree

def import_data():
    con  = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="000012300"
        )
    cur = con.cursor()
    cur.execute("USE mini_data")
    cur.execute("SELECT code from symptoms ORDER BY code")
    ##variables
    diseaseCodes = []
    symptomCode = []
    relations=[]

    for i in cur:
        symptomCode.append(i[0])

    cur.execute("SELECT code from diseases ORDER BY code")
    for i in cur:
        diseaseCodes.append(i[0])

    relations =  np.zeros((len(diseaseCodes), len(symptomCode)))

    for i in diseaseCodes:
        cur.execute("SELECT symptom_code from disease_symptom WHERE disease_code= '"+i+" '")
        for k in cur:
            relations[diseaseCodes.index(i)][symptomCode.index(k[0])]=1
        
    # for i in range(len(diseaseCodes)):
    #     print(diseaseCodes[i],end="\t")
    #     for j in range(len(symptomCode)):
    #         print(relations[i][j],end =" ")
    return diseaseCodes,symptomCode,relations


diseaseCodes,symptomCode,relations = import_data()
print(relations.shape)
clf = tree.DecisionTreeClassifier(criterion='entropy', splitter='best')
clf = clf.fit(relations,diseaseCodes)

print(clf.predict([relations[10]]))
print(diseaseCodes[10])
tree.plot_tree(clf)
print()

