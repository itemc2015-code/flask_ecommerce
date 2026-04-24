from  flask import Blueprint,jsonify,render_template,current_app

product_blueprint = Blueprint('product',__name__)

@product_blueprint.route('/product_list',methods=['GET'])
def product_lists():
    view_product = current_app.config['list_of_product']
    try:
        view_lists = view_product.product_list()
        return render_template('main.html',view_lists=view_lists)
    except:
        return jsonify({'message':'empty'})
