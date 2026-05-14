from flask import request,jsonify
from functools import wraps
from jose import jwt


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token missing'}), 401
        try:
            token = token.split(" ")[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except:
            return jsonify({'message': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated

@product_blueprint.route('/delete/<int:id>', methods=['DELETE'])
@token_required
def delete_product(id):
    return jsonify({'message':'deleted'})