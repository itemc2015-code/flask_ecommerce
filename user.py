from flask import Blueprint,current_app,request,jsonify
from passlib.hash import sha256_crypt
from flasgger import swag_from
from jose import jwt
import os
from dotenv import load_dotenv
from datetime import datetime,timedelta

user_blueprint = Blueprint('user',__name__)
load_dotenv()
ALGORITHM = 'HS256'
SECRET_KEY = os.getenv('secrets')
exp_time = 20

@user_blueprint.route('/signup',methods=['POST'])
@swag_from('docs/auth.yml')
def user_signup():
    user_request = current_app.config['list_of_users']
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not str(username).strip():
        return jsonify({'message':'username cannot be blank'}),400
    if not password or not str(password).strip():
        return jsonify({'message':'password cannot be blank'}),400
    hash_pwd = sha256_crypt.hash(password)
    if_match = user_request.get_username(username)
    if if_match:
        return jsonify({'message':'username already exist'}),400
    user_request.add_user(username,hash_pwd,role='user')
    return jsonify({'message':'successfully added'}),200

@user_blueprint.route('/login',methods=['POST'])
@swag_from('docs/auth.yml')
def user_login():
    user_request = current_app.config['list_of_users']
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    get_user = user_request.get_username(username)
    if not get_user:
        return jsonify({'message':'user does not exist'})
    status = get_user.get('is_active')

    if not status:
        return jsonify({'message':'user is inactive'}),401
    if not username or not str(username).strip() or not password or not str(password).strip():
        return jsonify({'message':'username and password cannot be blank'}),400
    if not get_user:
        return jsonify({'message':'username not found'}),400
    verify_pwd = sha256_crypt.verify(password,get_user['pwd'])
    if not verify_pwd:
        return jsonify({'message':'wrong password'}),400
    expire_time = datetime.utcnow() + timedelta(minutes=exp_time)
    for_payload = {"id":get_user.get('user_id'),"username":get_user.get('username'),"role":get_user.get('role'),"exp":expire_time}
    token = jwt.encode(for_payload,SECRET_KEY,algorithm=ALGORITHM)
    return jsonify({'access_token':token,'token_type':'bearer'})


