import logging, json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, abort, marshal
from blueprints.users import *
# from blueprints.admin import *
# ===== Untuk token =====
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

bp_auth = Blueprint('auth',__name__)
api = Api(bp_auth)

class CreateTokenResources(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()
        token_data = Users.query.filter_by(username=args['username']).filter_by(password=args['password']).first()
        
        # ==========(sentralize)==========
        if token_data is not None:
            token = create_access_token(marshal(token_data, Users.response_field))
            return{ 'username': token_data.username, 'type': token_data.type, 'token': token }, 200
        else:
            return{ 'status': 'UNAUTHORIZED', 'message': 'Invalid username or password' }, 401

api.add_resource(CreateTokenResources, '')