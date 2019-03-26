import logging, json, random
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
# ===== Untuk import db =====
from blueprints import db
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints.client import *
from blueprints.auth import *

# ===== Untuk import __init__.py =====
from . import *

bp_courier = Blueprint('courier', __name__)
api = Api(bp_courier)


#### book RESOURCE CLASS
#### All Data
class CourierResource(Resource):
    @jwt_required
    def get(self, id=None):
        if id == None:
            if get_jwt_claims()['type'] == 'client' or get_jwt_claims()['type'] == 'admin' or get_jwt_claims()['type'] == "superadmin":
                parser = reqparse.RequestParser()
                parser.add_argument('p', location='args', type=int, default=1)
                parser.add_argument('rp', location='args', type=int, default=5)
                args = parser.parse_args()

                # Rumus (p*rp)-rp
                offset = (args['p'] * args['rp']) - args['rp']
                
                # Memunculkan data semua (ditampilkan sesuai jumlah rp)
                courier_all = Couriers.query
                get_all = []
                for get_data in courier_all.limit(args['rp']).offset(offset).all():
                    get_all.append(marshal(get_data, Couriers.response_field))
                return get_all, 200, { 'Content-Type': 'application/json' }
            
        else:
            if get_jwt_claims()['type'] == 'client' or get_jwt_claims()['type'] == 'admin' or get_jwt_claims()['type'] == "superadmin":
                courier = Couriers.query.get(id)
                if courier is not None:
                    return marshal(courier, Couriers.response_field), 200, { 'Content-Type': 'application/json' }
                return {'status': 'NOT_FOUND', 'message': 'Anda belum membeli apapun'}, 404, { 'Content-Type': 'application/json' }

    @jwt_required
    def post(self):
        if get_jwt_claims()['type'] == 'admin' or get_jwt_claims()['type'] == "superadmin":
            parser = reqparse.RequestParser()
            parser.add_argument('nama_kurir', location='json', required=True)
            parser.add_argument('mode_pengiriman', location='json', required=True)
            parser.add_argument('image', location='json', required=True)
            args = parser.parse_args()
            
            # ==========(sentralize)==========
            courier = Couriers(None, args['nama_kurir'], args['mode_pengiriman'], args['image'])
            db.session.add(courier)
            db.session.commit()
            return marshal(courier, Couriers.response_field), 200, { 'Content-Type': 'application/json' }
        return { 'status': 'ADMIN_ONLY', 'message': 'Only allowed for admin' }, 404, { 'Content-Type': 'application/json' }

    @jwt_required
    def put(self, id=None):
        if get_jwt_claims()['type'] == 'admin' or get_jwt_claims()['type'] == "superadmin":
            parser = reqparse.RequestParser()
            parser.add_argument('id', location='json', type=int, required=True)
            parser.add_argument('nama_kurir', location='json')
            parser.add_argument('mode_pengiriman', location='json')
            parser.add_argument('image', location='json')
            args = parser.parse_args()
            
            # ambil dari resi json
            courier = Couriers.query.get(args['id'])
            temp = courier
                # ==========(sentralize)=========            
            if courier == None:
                return {'status':'NOT_AVAILABLE', 'message':'The courier is not available'}, 200, { 'Content-Type': 'application/json' }
                
            if courier != None:
                if args['nama_kurir'] != None:
                    courier.nama_kurir = args['nama_kurir']
                if args['mode_pengiriman'] != None:
                    courier.mode_pengiriman = args['mode_pengiriman']
                if args['image'] != None:
                    courier.image = args['image']
                
                if courier.nama_kurir == None:
                    courier.nama_kurir = temp['nama_kurir']
                if courier.mode_pengiriman == None:
                    courier.mode_pengiriman = temp['mode_pengiriman']
                if courier.image == None:
                    courier.image = temp['image']

                db.session.commit()
                return marshal(courier, Couriers.response_field), 200, { 'Content-Type': 'application/json' }
        return {'status': 'ADMIN_ONLY', 'message': 'Only for Admin'}, 404, { 'Content-Type': 'application/json' }

    @jwt_required
    def delete(self, id=None):
        if get_jwt_claims()['type'] == 'admin' or get_jwt_claims()['type'] == "superadmin":
            parser = reqparse.RequestParser()
            parser.add_argument('id', location='json', type=int)
            args = parser.parse_args()

            if id == None:
                courier = Couriers.query.get(args['id'])
            if id != None:
                courier = Couriers.query.get(id)

            if courier == None:
                return { 'status':'NOT_FOUND', 'message': 'Courier data not found' }, 200, { 'Content-Type': 'application/json' }
            if courier != None:
                db.session.delete(courier)
                db.session.commit()
                return { 'status':'COMPLETE', 'message': 'Delete complete' }, 200, { 'Content-Type': 'application/json' }
        return {'status': 'ADMIN_ONLY', 'message': 'Only for Admin'}, 404, { 'Content-Type': 'application/json' }


api.add_resource(CourierResource,'', '/<int:id>')