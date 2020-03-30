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

def getDiseaseDetails(code):
    cur.execute("use mini_data")
    q = "SELECT details from diseases where code = '{}' ".format(code)
    cur.execute(q)
    for i in cur:
        return(i[0])
    return "No info found"

def getSymptomDetails(code):
    cur.execute("use mini_data")
    q = "SELECT details from symptoms where code = '{}' ".format(code)
    cur.execute(q)
    for i in cur:
        return(i[0])
    return "No info found"
    

def print_disease_info(code):
    print("Name: \t{}".format(getDiseaseName(code)))

    print("Details:\t{}".format(getDiseaseDetails(code)))


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

def startTest():
    tree = clf.tree_
    node = 0      #Index of root node
    while True:
        feat,thres = tree.feature[node],tree.threshold[node]
        print(feat,thres)
        print()
        print("Select 1 for yes 0 for no and 3 to get more info")
        v = float(input("Do you have {}".format(getSymptomName(symptomCode[feat]))))
        if(v==3):
            print("Info: \n{}\n\n".format(getSymptomDetails(symptomCode[feat])))
            v = float(input("Do you have {}".format(getSymptomName(symptomCode[feat]))))
        if v<=thres:
            node = tree.children_left[node]
        else:
            node = tree.children_right[node]
        if tree.children_left[node] == tree.children_right[node]: #Check for leaf
            label = np.argmax(tree.value[node])
            print("\n\nDisease detected..")
            print("Predicted disease is:{} ".format(getDiseaseName(diseaseCodes[label])))
            print_disease_info(diseaseCodes[label])
            break

def getNext(options=[]):
    tree = clf.tree_
    node = 0      #Index of root node
    result=dict()
    if len(options)==0:
        feat,thres = tree.feature[node],tree.threshold[node]
        result["found"] = 0
        result["symptom_code"]=symptomCode[feat]
        result["symptom_name"]=getSymptomName(symptomCode[feat])
        result["symptom_details"]=getSymptomDetails(symptomCode[feat])
        return result

    for v,ind in zip(options,range(len(options))):
        feat,thres = tree.feature[node],tree.threshold[node]
        if v<=thres:
            node = tree.children_left[node]
        else:
            node = tree.children_right[node]
        if tree.children_left[node] == tree.children_right[node]: #Check for leaf
            label = np.argmax(tree.value[node])
            print("\n\nDisease detected..")
            print("Predicted disease is:{} ".format(getDiseaseName(diseaseCodes[label])))
            print_disease_info(diseaseCodes[label])
            result["found"] = 1
            result["disease_code"]=diseaseCodes[label]
            result["disease_name"]=getDiseaseName(diseaseCodes[label])
            result["disease_details"] = getDiseaseDetails(diseaseCodes[label])
            return result
        if ind+1==len(options):
            result["found"] = 0
            result["symptom_code"]=symptomCode[feat]
            result["symptom_name"]=getSymptomName(symptomCode[feat])
            result["symptom_details"]=getSymptomDetails(symptomCode[feat])
            return result

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

# To test if the code is working 
l=getNext([0,0,0,0,0,0,0,0,0,0,0,0,0,00,0,0,00,0,0,0,0,00,0,0,0,0,0,0,00,0,0,])
for i in l:
    print(i,l[i])