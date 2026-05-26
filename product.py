from  flask import Blueprint,jsonify,render_template,current_app
from flasgger import swag_from
from verify import token_required

product_blueprint = Blueprint('product',__name__)

@product_blueprint.route('/product_list',methods=['GET'])
@token_required
@swag_from('docs/product.yml')
def product_lists(current_user):
    view_product = current_app.config['list_of_product']
    try:
        view_lists = view_product.product_list()
        return view_lists
        # return render_template('main.html',view_lists=view_lists)
    except:
        return jsonify({'message':'empty'})
