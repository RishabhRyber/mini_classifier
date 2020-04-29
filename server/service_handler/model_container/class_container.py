import mysql.connector
from service_handler.model_container import temp
class question_session:
    def __init__(self,id=-1,email="dummy@funny.com"):
        self.id=id
        self.email=email
        self.con = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="000012300"
            )
        self.cur = self.con.cursor()
        self.choices = []


    def fetch_info(self,option=-1):
        self.cur.execute("USE mini_data")
        if self.id == -1:
            print("lol")
            self.cur.execute("SELECT max(id) from question_session")
            for i in self.cur:
                if type(i[0])  == type(None):
                    self.id=1
                else:   
                    self.id=i[0]+1
            self.cur.execute("INSERT INTO question_session(id,email) VALUES({},'{}')".format(self.id,self.email))
            self.con.commit()
            
        else:
            self.cur.execute("SELECT * from question_session where id = '{}'".format(self.id))
            for i in self.cur:
                print(i)
                if type(i[1])  == type(None):
                    self.choices=[option,]
                    break
                else:
                    self.email=i[2]
                    s=i[1].replace('[','')
                    s=s.replace(']','')
                    s=s.replace(', ','')
                    self.choices = [int(x) for x in s]+[option]                
                    print(self.choices)

    def getResponse(self):
        res=temp.getNext(self.choices)
        res["id"] = self.id
        return res


    def return_id(self):
        return self.id
    
    def save_email(self):
        self.cur.execute("UPDATE question_session set email = '{}'  where id = '{}'".format(self.email,self.id))
        self.con.commit()
    
    def save_options(self):
        self.cur.execute("UPDATE question_session set options = '{}'  where id = '{}'".format(self.choices,self.id))
        
        self.con.commit()
