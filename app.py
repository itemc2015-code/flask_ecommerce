from flask import Flask,jsonify
from product import product_blueprint
from user import user_blueprint
from ecommercedb import Products,Users
from passlib.context import CryptContext
from passlib.hash import sha256_crypt
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)
app.register_blueprint(product_blueprint,url_prefix='/product')
app.register_blueprint(user_blueprint,url_prefix='/user')
app.config['list_of_product'] = Products()
app.config['list_of_users'] = Users()
pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

def create_admin(role='user'):
    add_admin = app.config['list_of_users']
    get_user = add_admin.user_querry()
    if not get_user:
        username = 'admin'
        pwd = '1234'
        hash_pwd = sha256_crypt.hash(pwd)
        role = 'admin'
        add_admin.add_user(username,hash_pwd,role)

@app.before_first_request
def startup_event():
    create_admin()

if __name__ == '__main__':
    app.run(debug=True)

"""
USERS/ADMIN
#create default admin on start
/sign_up,/login
normal - view products,add to cart,update order,delete order,checkout
	 register,login,change password
admin - view products,update product list,delete product
	delete user,update password of user 

DATABASE
users > orders > order_items
users > products
products > order_items
orders > order_items

BACKEND (ROUTES)
order
/create_order
/update
/delete
/checkout
/view_order_summary

products
/view_products
/delete_products - admin
/update_products - admin

user
/register
/change_password
/delete_user - admin
/update_password_of_any_user - admin

AUTHENTICATION
generate token
protect routes

HTML (BASIC DISPLAY) 
"""