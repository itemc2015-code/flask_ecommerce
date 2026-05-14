from flask import Blueprint,current_app,request,jsonify
from flasgger import swag_from

order_blueprint = Blueprint("order",__name__)

@order_blueprint.route('/order',methods=['POST'])
@swag_from('docs/order.yml')
def add_to_cart():
    order_lists = current_app.config['list_of_order']
    get_products = current_app.config['list_of_product']
    get_user = current_app.config['list_of_users']
    data = request.get_json() or {}
    prod_id = data.get('prod_id')
    quantity = data.get('quantity')
    temp_user = get_user.get_username(username='temp_user')
    view_product = get_products.get_product(prod_id)

    if not prod_id or not str(prod_id).strip():
        return jsonify({'message':'input product id'}),400
    if not view_product:
        return jsonify({'message':'product id not found'}), 400
    view_orders = order_lists.view_orders()
    next_orders_id = max((v['order_id'] for v in view_orders),default=0) + 1
    total_order = quantity * view_product['price']
    order_lists.add_to_order_item(next_orders_id,view_product['product_id'],quantity,total_order,view_product['price'])
    grand_total = sum(total_order)
    order_lists.add_to_order(temp_user['user_id'],grand_total)
    # print(order_lists.view_orders())
    # print(view_product)
    return {'message':'successfully added'}

#ADD TO ORDER: update order items and orders
#error on inputing quantiy on order

