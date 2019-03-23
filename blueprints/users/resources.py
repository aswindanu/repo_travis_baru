import random, logging
from blueprints import db
import logging, json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, abort, marshal,fields
# ===== Untuk token =====
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

bp_user = Blueprint('user',__name__)
api = Api(bp_user)

#### data RESOURCE CLASS
#### All Data
class UserResource(Resource):
    # for client see their own ID/ admin for see all ID
    @jwt_required
    def get(self, id=None):
        if id == None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', location='args', type=int, default=1)
            parser.add_argument('rp', location='args', type=int, default=5)
            parser.add_argument('name', location='args')
            args = parser.parse_args()

            # Rumus (p*rp)-rp
            offset = (args['p'] * args['rp']) - args['rp']

            # Memunculkan data semua (ditampilkan sesuai jumlah rp)
            qry_all = Datas.query
            get_all = []

            if args['name'] is not None:
                qry_all = qry_all.filter(Datas.id.like("%"+args['name']+"%"))

            if get_jwt_claims()['type'] == "admin":
                for get_data in qry_all.limit(args['rp']).offset(offset).all():
                    get_all.append(marshal(get_data, Datas.response_field))
                return get_all, 200, {'Content-Type': 'application/json' }
            
            if get_jwt_claims()['type'] == "client" or get_jwt_claims()['type'] == "admin":
                qry = Datas.query.get(get_jwt_claims()['id'])
                return marshal(qry, Datas.response_field), 200, { 'Content-Type': 'application/json' }
            
        else:
            qry = Datas.query.get(id)
            if qry is not None:
                if get_jwt_claims()['type'] == "client" or get_jwt_claims()['type'] == "admin":
                    return marshal(qry, Datas.response_field), 200, { 'Content-Type': 'application/json' }
            return {'status': 'NOT_FOUND', 'message': 'Book not found'}, 404, { 'Content-Type': 'application/json' }

api.add_resource(UserResource, '')