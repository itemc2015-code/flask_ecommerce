from flask import Blueprint,current_app,request,jsonify
from flasgger import swag_from
from verify import token_required

order_blueprint = Blueprint("order",__name__)

@order_blueprint.route('/order',methods=['POST'])
@token_required
@swag_from('docs/order.yml')
def add_to_cart(current_user):
    order_lists = current_app.config['list_of_order']
    get_products = current_app.config['list_of_product']

    data = request.get_json() or {}
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    product_lists = get_products.product_list()
    get_product_id = [p['product_id'] for p in product_lists]
    get_this_product = get_products.get_product(product_id)

    if not product_id or not str(product_id).strip():
        return jsonify({'message':'input product id'}),400
    if not quantity:
        return jsonify({'message':'input quantity'}),400
    if quantity <= 0:
        return jsonify({'message':'quantity must be greater than 0'}),400
    if product_id not in get_product_id:
        return jsonify({'message':'product id not found'}),400

    user_id = current_user.get('id')
    total = quantity *  get_this_product.get('price')
    has_pending = order_lists.has_pending_order(user_id)

    if has_pending:
        order_id = has_pending.get('order_id')
        price = get_this_product.get('price')
        item_name = get_this_product.get('item_name')
        order_lists.add_to_order_item(order_id, product_id, quantity, total, price, item_name)
        order_grand_total = order_lists.get_order(order_id)
        grand_total = order_lists.get_grand_total(order_id)
        order_grand_total = grand_total
        total_order_count = order_lists.total_order_count(order_id)
        current_order_count = order_lists.get_order_count(order_id)
        current_order_count = total_order_count
        order_lists.update_order_count(order_id,current_order_count)
        order_lists.grand_total(order_id,order_grand_total)
        return jsonify({'message': 'cart updated succefully'})
    order_id = order_lists.add_to_order(user_id)
    price = get_this_product.get('price')
    item_name = get_this_product.get('item_name')
    order_lists.add_to_order_item(order_id,product_id,quantity,total,price,item_name)
    return jsonify({'message':'item added to cart'})

@order_blueprint.route('/view_orders',methods=['GET'])
@token_required
@swag_from('docs/view_order.yml')
def view_order(current_user):
    user_id = current_user.get('user_id')
    order_service = current_app.config['list_of_order']
    order_items = order_service.all_order_items()
    order_service.view_orders(user_id,)
    order_id = [o['order_id'] for o in order_items]
    get_order_id = order_service.has_pending_order(user_id)

    if not order_items:
        return jsonify({'message':'cart is empty'})
    print(order_id)
    return order_items


#ALWAYS UPDATE GIT, add no. of items, view orders

'''
normal - #view products
         #add to cart
         update order
         delete order
         checkout
	     register
	     login
	     change password
	     
[
  {
    "id": 7,
    "role": "user",
    "username": "luffy"
  },
  {
    "id": 9,
    "role": "user",
    "username": "usoff"
  },
  {
    "id": 12,
    "role": "admin",
    "username": "brook"
  },
  {
    "id": 13,
    "role": "admin",
    "username": "admin"
  },
  {
    "id": 14,
    "role": "user",
    "username": "chopper"
  }
]
'''