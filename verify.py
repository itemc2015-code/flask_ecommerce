from flask import request,jsonify
from functools import wraps
from jose import jwt,JWTError,ExpiredSignatureError
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('secrets')
ALGORITHM = 'HS256'

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({'message':'token not found'}),401
        try:
            token = token.split(" ")[1]
            data = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        except ExpiredSignatureError:
            return jsonify({'message':'token expired'}),401
        except JWTError:
            return jsonify({'message':'invalid token'}),401
        return f(data,*args,**kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(current_user,*args,**kwargs):
        get_role = current_user.get('role')
        if get_role != 'admin':
            return jsonify({'message':'no permission'}),403
        return f(current_user,*args,**kwargs)
    return decorated