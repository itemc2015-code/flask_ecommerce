from flask import Flask,jsonify
from product import product_blueprint
from user import user_blueprint
from order import order_blueprint
from admin import admin_blueprint
from ecommercedb import Products,Users,Orders
from passlib.context import CryptContext
from passlib.hash import sha256_crypt
from flasgger import Swagger

app = Flask(__name__)
Swagger(app, template={
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Bearer <JWT token>"
        }
    }
})

app.register_blueprint(product_blueprint,url_prefix='/product')
app.register_blueprint(user_blueprint,url_prefix='/user')
app.register_blueprint(order_blueprint,url_prefix='/order')
app.register_blueprint(admin_blueprint,url_prefix='/admin')
app.config['list_of_product'] = Products()
app.config['list_of_users'] = Users()
app.config['list_of_order'] = Orders()
pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

def create_admin(role='user'):
    add_admin = app.config['list_of_users']
    data = add_admin.user_querry()
    get_user = [d['username'] for d in data]
    if 'admin' not in get_user:
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
#/sign_up for normal user,#/login
normal - #view products
         add to cart
         update order
         delete order
         checkout
	     register
	     login
	     change password
admin - #view products
        update product list
        delete product
	    #delete user
	    #update password of user 
	    #create user, role is admin

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