from flask import Blueprint,current_app,jsonify,request
from flasgger import swag_from
from verify import token_required,admin_required
from passlib.hash import sha256_crypt

admin_blueprint = Blueprint('admin',__name__)

@admin_blueprint.route('/view_users',methods=['GET'])
@token_required
@admin_required
@swag_from('docs/user.yml')
def users_view(current_user):
    try:
        view_user_list = current_app.config['list_of_users']
        view_user_lists = view_user_list.user_querry()
        view_user_lists1 = [{'id':v['user_id'],'username':v['username'],'role':v['role'],'status':'active'if v['is_active'] else 'inactive'} for v in view_user_lists]
        return view_user_lists1
    except:
        return jsonify({'message':'empty'})

@admin_blueprint.route('/delete_user',methods=['POST'])
@token_required
@admin_required
@swag_from('docs/delete_user.yml')
def user_delete(current_user):
    get_user = current_app.config['list_of_users']
    get_users = get_user.user_querry()
    get_id = [g['user_id'] for g in get_users]
    get_user_id = request.get_json() or {}
    get_user_id = get_user_id.get('id')
    if get_user_id not in get_id:
        return jsonify({'message':'user id not found'}),403
    get_user.delete_user(get_user_id)
    return jsonify({'message':'user deleted'})

@admin_blueprint.route('/update_password',methods=['PUT'])
@token_required
@admin_required
@swag_from('docs/update_pwd.yml')
def user_password(current_user):
    get_user = current_app.config['list_of_users']
    get_data = request.get_json() or {}
    username = get_data.get('username')
    password = get_data.get('password')
    if_match_username = get_user.get_username(username)
    if not if_match_username:
        return jsonify({'message':'username not found'}),403
    hash_pwd = sha256_crypt.hash(password)
    get_user.update_password(username,hash_pwd)
    return jsonify({'message':'password successfully updated'})

@admin_blueprint.route('/create_admin_user',methods=['POST'])
@token_required
@admin_required
@swag_from('docs/create_admin.yml')
def admin_user(current_user):
    data = current_app.config['list_of_users']
    get_data = request.get_json() or {}
    username = get_data.get('username')
    password = get_data.get('password')
    if_match_username = data.get_username(username)
    if not username or not str(username).strip():
        return jsonify({'message':'username cannot be blank'}),400
    if not password or not str(password).strip():
        return jsonify({'message': 'password cannot be blank'}), 400
    if if_match_username:
        return jsonify({'message':'username already exist'}),400
    hash_pwd = sha256_crypt.hash(password)
    role = 'admin'
    data.add_user(username,hash_pwd,role)
    return jsonify({'message':'new admin role successfully added'})

@admin_blueprint.route('/update_product',methods=['PUT'])
@token_required
@admin_required
@swag_from('docs/product_update.yml')
def update_product(current_user):
    data = current_app.config['list_of_product']
    get_input = request.get_json() or {}
    product_id = get_input.get('product_id')
    item_name = get_input.get('item_name')
    stock_quantity = get_input.get('stock_quantity')
    price = get_input.get('price')
    get_prod_id = data.get_product(product_id)
    if not get_prod_id:
        return jsonify({'message':'product id not found'}),404
    item_name = get_prod_id['item_name'] if not item_name else item_name
    stock_quantity = get_prod_id['stock_quantity'] if not stock_quantity else stock_quantity
    price = get_prod_id['price'] if not price else price
    data.update_product(product_id,item_name,stock_quantity,price)
    return jsonify({'message':'successfully updated'})

@admin_blueprint.route('delete_product',methods=['DELETE'])
@token_required
@admin_required
@swag_from('docs/delete_product.yml')
def product_delete(current_user):
    data = current_app.config['list_of_product']
    get_input = request.get_json() or {}
    product_id = get_input.get('product_id')
    get_product_id = data.get_product(product_id)
    if not get_product_id:
        return jsonify({'message':'product id not found'}),404
    data.delete_product(product_id)
    return jsonify({'message':'successfully deleted'})

@admin_blueprint.route('/disable_user',methods=['PUT'])
@token_required
@admin_required
@swag_from('docs/disable_user.yml')
def disable_user(current_user):
    get_input = request.get_json() or {}
    user_id_input = get_input.get('user_id')
    user_service = current_app.config['list_of_users']
    if_inactive = user_service.if_user_inactive(user_id_input)
    get_users = user_service.user_querry()
    users_list = [g['user_id'] for g in get_users]

    if not user_id_input:
        return jsonify({'message':'input used id to deactivate'})
    if user_id_input not in users_list:
        return jsonify({'message':'user id not found'})
    if if_inactive:
        return jsonify({'message':'user already inactive'})

    user_service.disable_user(user_id_input)
    return jsonify({'message':'user is inactive'})

@admin_blueprint.route('/activate_user',methods=['PUT'])
@token_required
@admin_required
@swag_from('docs/activate_user.yml')
def activate_user(current_user):
    user_service = current_app.config['list_of_users']
    get_input = request.get_json() or {}
    user_id_input = get_input.get('user_id')
    if not user_id_input:
        return jsonify({'message':'input user id to activate'})
    get_users = user_service.user_querry()
    users_list = [g['user_id'] for g in get_users]
    if user_id_input not in users_list:
        return jsonify({'message':'user id not found'}),404
    if_user_active = user_service.if_user_active(user_id_input)
    if if_user_active:
        return jsonify({'message': 'user already active'}),400
    user_service.enable_user(user_id_input)
    return jsonify({'message': 'user is active'})

#create route for activate user