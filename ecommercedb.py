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

    def create_admin(self):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'insert into users(username,pwd)'

    def add_user(self,username,pwd,role):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'insert into users(username,pwd,role) values(%s,%s,%s)'
        dbcursor.execute(query,(username,pwd,role,))
        dbcursor.close()
        self.db.commit()

    def get_username(self,username):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True)
        query = 'select * from users where username = %s'
        dbcursor.execute(query,(username,))
        result = dbcursor.fetchone()
        return result
