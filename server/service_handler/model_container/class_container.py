import mysql.connector

class question_session:
    def __init__(self,id=-1,email="dummy@funny.com",option=-1):
        self.id=id
        self.email=email
        self.con = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="000012300"
            )
        self.cur = self.con.cursor()
        self.choices = []


    def fetch_info(self):
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

    def getResponse(self):
        for i in self.choices:


    def return_id(self):
        return self.id
    