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
        view_user_lists1 = [{'id':v['user_id'],'username':v['username'],'role':v['role']} for v in view_user_lists]
        return view_user_lists1
    except:
        return jsonify({'message':'empty'})

@admin_blueprint.route('/delete_user',methods=['POST'])
@swag_from('docs/delete_user.yml')
def user_delete():
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


#TO BE CONTINUE: update user pwd, admin only, update repo
                #put authentication first on all route
                #test all route
                #create user, role is admin

'''admin - #view products
        update product list
        delete product
	    #delete user
	    update password of user '''

