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

    customer_name = current_user.get('username')
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
    # get_prod_id = order_lists.view_user_orders(has_pending['order_id'])
    # prod_id = [g['product_id'] for g in get_prod_id]
    # if product_id in prod_id:
    #     return jsonify({'message':'item already added, use update to change quantity'})

    if has_pending:
        order_id = has_pending.get('order_id')
        price = get_this_product.get('price')
        item_name = get_this_product.get('item_name')

        get_order_product_id = order_lists.get_order_items(order_id)
        order_product_id = [g['product_id'] for g in get_order_product_id]

        if product_id in order_product_id:
            # order_lists.update_quantity_total(product_id,quantity,total)
            # order_grand_total = order_lists.get_order(order_id)  # GET GRAND TOTAL FROM ORDERS TABLE
            # grand_total = order_lists.get_grand_total(order_id)  # SUM OF TOTAL FROM ORDER ITEMS TABLE
            # order_grand_total = grand_total
            # order_lists.grand_total(order_id, order_grand_total)  # UPDATE GRAND TOTAL ON ORDERS TABLE
            return jsonify({'message':'item already added, use update to change quantity'})

        order_lists.add_to_order_item(order_id, product_id, quantity, total, price, item_name)
        order_grand_total = order_lists.get_order(order_id) #GET GRAND TOTAL FROM ORDERS TABLE
        grand_total = order_lists.get_grand_total(order_id) #SUM TOTAL FROM ORDER ITEMS TABLE
        order_grand_total = grand_total
        total_order_count = order_lists.total_order_count(order_id) #GET ITEM COUNT ON ORDER ITEMS
        current_order_count = order_lists.get_order_count(order_id) #CALL ORDER COUNT FROM ORDER TABLE FOR UPDATING
        current_order_count = total_order_count
        order_lists.update_order_count(order_id,current_order_count) #UPDATE ORDER COUNT ON ORDERS TABLE
        order_lists.grand_total(order_id,order_grand_total) #UPDATE GRAND TOTAL ON ORDERS TABLE
        return jsonify({'message': 'cart updated succefully'})

    order_id = order_lists.add_to_order(user_id,customer_name)
    price = get_this_product.get('price')
    item_name = get_this_product.get('item_name')
    order_lists.add_to_order_item(order_id,product_id,quantity,total,price,item_name)

    order_grand_total = order_lists.get_order(order_id)  # GET GRAND TOTAL FROM ORDERS TABLE
    grand_total = order_lists.get_grand_total(order_id)  # SUM TOTAL FROM ORDER ITEMS TABLE
    order_grand_total = grand_total
    total_order_count = order_lists.total_order_count(order_id)  # GET ITEM COUNT ON ORDER ITEMS
    current_order_count = order_lists.get_order_count(order_id)  # CALL ORDER COUNT FROM ORDER TABLE FOR UPDATING
    current_order_count = total_order_count
    order_lists.update_order_count(order_id, current_order_count)  # UPDATE ORDER COUNT ON ORDERS TABLE
    order_lists.grand_total(order_id, order_grand_total)  # UPDATE GRAND TOTAL ON ORDERS TABLE

    return jsonify({'message':'item added to cart'})

@order_blueprint.route('/view_orders',methods=['GET'])
@token_required
@swag_from('docs/view_order.yml')
def view_order(current_user):
    user_id = current_user.get('id')
    order_services = current_app.config['list_of_order']
    get_order_id = order_services.pending_order(user_id)

    if not get_order_id:
        return jsonify({'message':'cart is empty'})

    order_id = get_order_id['order_id']
    orders = order_services.user_order(order_id)
    return orders

@order_blueprint.route('/order_update',methods=['PUT'])
@token_required
@swag_from('docs/order_update.yml')
def update_order(current_user):
    data = request.get_json() or {}
    product_id = data.get('product_id')
    quantity =  data.get('quantity')
    user_id = current_user.get('id')
    order_services = current_app.config['list_of_order']
    get_order_id = order_services.pending_order(user_id)

    if not get_order_id:
        return jsonify({'message':'cart is empty'})

    order_id = get_order_id.get('order_id')
    get_prod_id = order_services.get_order_items(order_id)
    if_match = [g['product_id'] for g in get_prod_id]

    if not product_id:
        return jsonify({'message':'product id cannot be blank'}),400
    if product_id not in if_match:
        return jsonify({'message':'item or product id not found'}),400
    if not quantity:
        return jsonify({'message':'input quantity'}),400
    if quantity <= 0:
        return jsonify({'message':'quantity must be greater than 0'})

    get_price = order_services.product_id_order_items(product_id)
    total = quantity * get_price['price']
    order_services.update_quantity_total(product_id,quantity,total)
    new_grand_total = order_services.get_grand_total(order_id)
    order_services.grand_total(order_id,new_grand_total)
    return jsonify({'message':'order updated'})

#ONGOING:
#ALWAYS UPDATE GIT

'''
normal - #view products
         #add to cart
         #view order
         update order
         delete order
         checkout
	     #register
	     #login
	     #change password
	     
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