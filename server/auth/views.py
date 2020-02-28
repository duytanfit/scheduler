from datetime import datetime

from flask import Blueprint, request, make_response, jsonify, session
from models.db_model import User
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, decode_token
import hashlib
from utils.mysql import MySql

jwt = JWTManager()
auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/auth/login', methods=['POST'])
def Login():
    post_data = request.get_json()
    username = post_data['user_name']
    user = MySql.get_user_by_user_name(username)
    if user and user.password == hashlib.sha256(post_data["password"].encode("utf-8")).hexdigest():
        access_token = create_access_token(identity=user.id, expires_delta=False)
        return jsonify(status="success", access_token=access_token), 200
    else:
        return jsonify(status="error", message="Usename or password is error"), 200

@jwt_required
def get_current_user(token):
    return decode_token(token)


@auth_blueprint.route('/auth/dangky', methods=['GET'])
def dang_ki():
    user = User('huynhtan06', hashlib.sha256('123456'.encode("utf-8")).hexdigest(), 2, first_name="HT06")
    MySql.save_to_db(user)
    print(user.password)
    return {
        "hello": "ok"
    }

@auth_blueprint.route('/auth/status', methods=['GET'])
def Status():
    # get the auth token
    auth_header = request.headers.get('Authorization')
    print(auth_header, flush=True)
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = User.query.filter_by(id=resp).first()
            responseObject = {
                'status': 'success',
                'data': {
                    'user_id': user.id,
                    'user_name': user.user_name,
                    'first_name': user.first_name,
                    'department_id': user.department_id
                }
            }
            return make_response(jsonify(responseObject)), 200
        responseObject = {
            'status': 'fail',
            'message': resp
        }
        return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 401
