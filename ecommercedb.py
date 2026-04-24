import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

class Dbconnect():
    db = mysql.connector.connect(
        host=os.getenv('dbhost'),
        user=os.getenv('dbuser'),
        password=os.getenv('dbpassword'),
        database=os.getenv('dbdatabase')
    )

class Products(Dbconnect):
    def product_list(self):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from product'
        dbcursor.execute(query)
        result = dbcursor.fetchall()
        dbcursor.close()
        return result

class Users(Dbconnect):
    def user_querry(self):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from users'
        dbcursor.execute(query)
        result = dbcursor.fetchall()
        return result

    def add_user(self,username,pwd):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'insert into users(username,pwd) values(%s,%s)'
        dbcursor.execute(query,(username,pwd,))
        dbcursor.close()
        self.db.commit()
