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

    def disable_user(self,user_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'update users set is_active = False where user_id = %s'
        dbcursor.execute(query,(user_id,))
        dbcursor.close()
        self.db.commit()

    def if_user_inactive(self,user_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from users where user_id = %s and is_active = False'
        dbcursor.execute(query,(user_id,))
        result = dbcursor.fetchone()
        dbcursor.close()
        return result

    def enable_user(self,user_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'update users set is_active = True where user_id = %s'
        dbcursor.execute(query,(user_id,))
        dbcursor.close()
        self.db.commit()

    def if_user_active(self,user_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from users where user_id = %s and is_active = True'
        dbcursor.execute(query,(user_id,))
        result = dbcursor.fetchone()
        dbcursor.close()
        return result


class Orders(Dbconnect):
    def view_orders(self,user_id,order_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from orders where user_id = %s and order_id = %s'
        dbcursor.execute(query,(user_id,order_id))
        result = dbcursor.fetchall()
        dbcursor.close()
        return result

    def view_user_orders(self,order_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from order_items where order_id = %s'
        dbcursor.execute(query,(order_id,))
        result = dbcursor.fetchall()
        dbcursor.close()
        return result

    def product_id_order_items(self,product_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from order_items where product_id = %s'
        dbcursor.execute(query,(product_id,))
        result = dbcursor.fetchone()
        dbcursor.close()
        return result

    def user_order(self,order_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = '''select oi.product_id,oi.item_name as item,oi.price,oi.quantity,oi.total from orders as o
                join order_items oi on o.order_id = oi.order_id
                where o.order_id = %s'''
        dbcursor.execute(query,(order_id,))
        result = dbcursor.fetchall()
        dbcursor.close()
        return result

    def all_order_items(self):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from order_items'
        dbcursor.execute(query)
        result = dbcursor.fetchall()
        dbcursor.close()
        return result

    def get_order(self,order_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from orders where order_id = %s'
        dbcursor.execute(query,(order_id,))
        result = dbcursor.fetchone()
        dbcursor.close()
        return result['grand_total']

    def add_to_order_item(self,order_id,product_id,quantity,total,price,item_name):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True)
        query = """insert into order_items(order_id,product_id,quantity,total,price,item_name)
                    values(%s,%s,%s,%s,%s,%s)"""
        dbcursor.execute(query,(order_id,product_id,quantity,total,price,item_name))
        self.db.commit()
        dbcursor.close()

    def add_to_order(self,user_id,customer_name):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True)
        query = """insert into orders(user_id,customer_name)
                values(%s,%s)"""
        dbcursor.execute(query,(user_id,customer_name))
        self.db.commit()
        order_id = dbcursor.lastrowid
        dbcursor.close()
        return order_id

    def has_pending_order(self,user_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from orders where user_id = %s and status = "pending"'
        dbcursor.execute(query,(user_id,))
        result = dbcursor.fetchone()
        dbcursor.close()
        return result

    def pending_order(self,user_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from orders where user_id = %s and status = "pending"'
        dbcursor.execute(query,(user_id,))
        result = dbcursor.fetchone()
        dbcursor.close()
        return result

    def get_order_items(self,order_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True)
        query = 'select * from order_items where order_id = %s'
        dbcursor.execute(query,(order_id,))
        result = dbcursor.fetchall()
        dbcursor.close()
        return result

    def get_grand_total(self,order_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select sum(total) as grand_total from order_items where order_id = %s'
        dbcursor.execute(query,(order_id,))
        result = dbcursor.fetchone()
        dbcursor.close()
        return result['grand_total']

    def grand_total(self,order_id,grandtotal):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'update orders set grand_total = %s where order_id = %s'
        dbcursor.execute(query,(grandtotal,order_id))
        dbcursor.close()
        self.db.commit()

    def total_order_count(self,order_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select count(total) as total_count from order_items where order_id = %s'
        dbcursor.execute(query,(order_id,))
        result = dbcursor.fetchone()
        dbcursor.close()
        return result['total_count']

    def update_order_count(self,order_id,order_count):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'update orders set order_count = %s where order_id = %s'
        dbcursor.execute(query,(order_count,order_id))
        dbcursor.close()
        self.db.commit()

    def get_order_count(self,order_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from orders where order_id = %s'
        dbcursor.execute(query,(order_id,))
        result = dbcursor.fetchone()
        dbcursor.close()
        return result['order_count']

    def update_quantity_total(self,product_id,quantity,total):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'update order_items set quantity = %s,total = %s where product_id = %s'
        dbcursor.execute(query,(quantity,total,product_id))
        dbcursor.close()
        self.db.commit()

    def delete_order(self,product_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'delete from order_items where product_id = %s'
        dbcursor.execute(query,(product_id,))
        dbcursor.close()
        self.db.commit()

    def for_checkout(self,order_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select order_id,date_time,order_count,grand_total from orders where order_id = %s'
        dbcursor.execute(query,(order_id,))
        result = dbcursor.fetchone()
        dbcursor.close()
        return result

    def update_status(self,order_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'update orders set status = "completed" where order_id = %s'
        dbcursor.execute(query,(order_id,))
        dbcursor.close()
        self.db.commit()

    def status_to_cancel(self,order_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'update orders set status = "cancel" where order_id = %s'
        dbcursor.execute(query,(order_id,))
        dbcursor.close()
        self.db.commit()

    def checkout(self):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from orders where order_id = %s'
        pass

