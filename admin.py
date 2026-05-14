from flask import Blueprint,current_app,jsonify
from flasgger import swag_from

admin_blueprint = Blueprint('admin',__name__)

@admin_blueprint.route('/view_users',methods=['GET'])
@swag_from('docs/user.yml')
def users_view():
    try:
        view_user_list = current_app.config['list_of_users']
        view_user_lists = view_user_list.user_querry()
        view_user_lists = [{'id':v['user_id'],'username':v['username'],'role':v['role']} for v in view_user_lists]
        return view_user_lists
    except:
        return jsonify({'message':'empty'})


#TO BE CONTINUE:
'''admin - view products
        update product list
        delete product
	    delete user
	    update password of user '''

