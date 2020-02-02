import pandas as pd
import mysql.connector
import numpy as np
from sklearn import tree
import pickle
import os.path

con  = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="000012300"
    )
cur = con.cursor()

def import_data():
    cur.execute("USE mini_data")
    cur.execute("SELECT code from symptoms ORDER BY code")
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
    return diseaseCodes,symptomCode,relations

#Utility Function to return name of disease from it's code
def getDiseaseName(code):
    cur.execute("use mini_data")
    q = "SELECT name from diseases where code = '{}' ".format(code)
    cur.execute(q)
    for i in cur:
        return(i[0])


#Utility Function to return name of symptom from it's code
def getSymptomName(code):
    cur.execute("use mini_data")
    q = "SELECT name from symptoms where code = '{}' ".format(code)
    cur.execute(q)
    for i in cur:
        return(i[0])

def save_classifer(clf,symptom_code,disease_code):
    file = open("classifier.pickle","wb")
    pickle.dump(clf,file)
    file.close()
    file = open("disease.pickle","wb")
    pickle.dump(disease_code,file)
    file.close()
    file = open("symptom.pickle","wb")
    pickle.dump(symptom_code,file)
    file.close()

def restore_classifier():
    file = open("classifier.pickle","rb")
    clf = pickle.load(file)
    file.close()
    file = open("disease.pickle","rb")
    disease = pickle.load(file)
    file.close()
    file = open("symptom.pickle","rb")
    symptom = pickle.load(file)
    file.close()
    return clf,disease,symptom

def startTest(clf):
    tree = clf.tree_
    node = 0      #Index of root node
    while True:
        feat,thres = tree.feature[node],tree.threshold[node]
        print(feat,thres)
        v = float(input("Do you have {}".format(getSymptomName(symptomCode[feat]))))
        if v<=thres:
            node = tree.children_left[node]
        else:
            node = tree.children_right[node]
        if tree.children_left[node] == tree.children_right[node]: #Check for leaf
            label = np.argmax(tree.value[node])
            print("We've reached a leaf")
            print("Predicted Label is:{} ,{}".format(diseaseCodes[label],getDiseaseName(diseaseCodes[label])))
            break


if(os.path.isfile("classifier.pickle")):
    clf,diseaseCodes,symptomCode = restore_classifier()
    print("using saved classifier")
else:
    print("not using saved classifier")
    diseaseCodes,symptomCode,relations = import_data()
    #classifer start
    clf = tree.DecisionTreeClassifier(criterion='entropy', splitter='best')
    clf = clf.fit(relations,diseaseCodes)
    #classifier done
    #demo prediction by whole feature set at once
    print(clf.predict([relations[10]]))
    print(diseaseCodes[10])
    save_classifer(clf,symptomCode,diseaseCodes)
startTest(clf)