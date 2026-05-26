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
    def get_product(self,product_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True)
        query = 'select * from product where product_id = %s'
        dbcursor.execute(query,(product_id,))
        result = dbcursor.fetchone()
        dbcursor.close()
        return result
    def update_product(self,product_id,item_name,stock_quantity,price):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'update product set item_name=%s,stock_quantity=%s,price=%s where product_id=%s'
        dbcursor.execute(query,(item_name,stock_quantity,price,product_id))
        dbcursor.close()
        self.db.commit()
    def delete_product(self,product_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'delete from product where product_id = %s'
        dbcursor.execute(query,(product_id,))
        dbcursor.close()
        self.db.commit()

class Users(Dbconnect):
    def user_querry(self):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from users'
        dbcursor.execute(query)
        result = dbcursor.fetchall()
        dbcursor.close()
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

    def delete_user(self,id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'delete from users where user_id = %s'
        dbcursor.execute(query,(id,))
        dbcursor.close()
        self.db.commit()

    def update_password(self,username,password):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'update users set pwd = %s where username = %s'
        dbcursor.execute(query,(password,username))
        dbcursor.close()
        self.db.commit()

class Orders(Dbconnect):
    def view_orders(self):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from orders'
        dbcursor.execute(query)
        result = dbcursor.fetchall()
        dbcursor.close()
        return result

    def add_to_order_item(self,order_id,product_id,quantity,total,price):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True)
        query = """insert into order_items(order_id,product_id,quantity,total,price)
                    values(%s,%s,%s,%s,%s)"""
        dbcursor.execute(query,(order_id,product_id,quantity,total,price,))
        self.db.commit()
        dbcursor.close()

    def add_to_order(self,user_id,grand_total):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True)
        query = """insert into orders(user_id,grand_total)
                values(%s,%s,%s)"""
        dbcursor.execute(query,(user_id,grand_total,))
        self.db.commit()
        dbcursor.close()

"""
[{'Tables_in_flask_ecommerce': 'order_items'},
[{'Field': 'id', 'Type': 'int(11)', 'Null': 'NO', 'Key': 'PRI', 'Default': None, 'Extra': 'auto_increment'},
{'Field': 'order_id', 'Type': 'int(11)', 'Null': 'YES', 'Key': 'MUL', 'Default': None, 'Extra': ''}, 
{'Field': 'product_id', 'Type':'int(11)', 'Null': 'YES', 'Key': 'MUL', 'Default': None, 'Extra': ''}, 
{'Field': 'quantity', 'Type': 'int(11)', 'Null': 'YES', 'Key': '', 'Default': None, 'Extra': ''}, 
{'Field': 'total', 'Type': 'float', 'Null': 'YES', 'Key': '', 'Default': None, 'Extra': ''}, 
{'Field': 'price', 'Type': 'float', 'Null': 'YES', 'Key': '', 'Default': None, 'Extra': ''}]

{'Tables_in_flask_ecommerce': 'orders'}, 
[{'Field': 'order_id', 'Type': 'int(11)', 'Null': 'NO', 'Key': 'PRI', 'Default': None, 'Extra': 'auto_increment'}, 
{'Field': 'user_id', 'Type': 'int(11)', 'Null': 'YES', 'Key': 'MUL', 'Default': None, 'Extra': ''}, 
{'Field': 'grand_total','Type': 'float', 'Null': 'YES', 'Key': '', 'Default': None, 'Extra': ''}, 
{'Field': 'price', 'Type': 'float', 'Null': 'YES', 'Key': '', 'Default': None, 'Extra': ''}]
"""
