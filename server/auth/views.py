from flask import Blueprint, request, make_response, jsonify, session
from flask.views import MethodView
from models.users import UsersModel

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/auth/login', methods=['POST'])
def Login():
    # get the post data
    post_data = request.get_json()
    try:
        # fetch the user data
        user = UsersModel.find_user_by_username(post_data.get('user_name'))
        if user:
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                session['login'] = user.id
                print(session['login'])
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User does not exist.'
            }
            return make_response(jsonify(responseObject)), 404
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(responseObject)), 500

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
        resp = UsersModel.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = UsersModel.query.filter_by(id=resp).first()
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

