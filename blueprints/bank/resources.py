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

bp_bank = Blueprint('bank', __name__)
api = Api(bp_bank)


#### book RESOURCE CLASS
#### All Data
class BankResource(Resource):
    @jwt_required
    def get(self, id=None):
        if id == None:
            # if get_jwt_claims()['type'] == 'client':
            parser = reqparse.RequestParser()
            parser.add_argument('p', location='args', type=int, default=1)
            parser.add_argument('rp', location='args', type=int, default=5)
            args = parser.parse_args()

            # Rumus (p*rp)-rp
            offset = (args['p'] * args['rp']) - args['rp']
            
            # Memunculkan data semua (ditampilkan sesuai jumlah rp)
            bank_all = Banks.query
            get_all = []
            for get_data in bank_all.limit(args['rp']).offset(offset).all():
                get_all.append(marshal(get_data, Banks.response_field))
            return get_all, 200, { 'Content-Type': 'application/json' }
            
        else:
            # if get_jwt_claims()['type'] == 'client':
            bank = Banks.query.get(id)
            if bank is not None:
                return marshal(bank, Banks.response_field), 200, { 'Content-Type': 'application/json' }
            return {'status': 'NOT_FOUND', 'message': 'Anda belum membeli apapun'}, 404, { 'Content-Type': 'application/json' }

    @jwt_required
    def post(self):
        if get_jwt_claims()['type'] == 'admin' or get_jwt_claims()['type'] == "superadmin":
            parser = reqparse.RequestParser()
            parser.add_argument('nama_bank', location='json', required=True)
            parser.add_argument('no_rekening', location='json', type=int, required=True)
            parser.add_argument('nama_pemilik', location='json', required=True)
            parser.add_argument('image', location='json', required=True)
            args = parser.parse_args()
            
            # ==========(sentralize)==========
            bank = Banks(None, args['nama_bank'], args['no_rekening'], args['nama_pemilik'], args['image'])
            db.session.add(bank)
            db.session.commit()
            return marshal(bank, Banks.response_field), 200, { 'Content-Type': 'application/json' }
        return { 'status': 'ADMIN_ONLY', 'message': 'Only allowed for admin' }, 404, { 'Content-Type': 'application/json' }

    @jwt_required
    def put(self, id=None):
        if get_jwt_claims()['type'] == 'admin' or get_jwt_claims()['type'] == "superadmin":
            parser = reqparse.RequestParser()
            parser.add_argument('id', location='json', type=int, required=True)
            parser.add_argument('nama_bank', location='json')
            parser.add_argument('no_rekening', location='json', type=int)
            parser.add_argument('nama_pemilik', location='json')
            args = parser.parse_args()
            
            # ambil dari resi json
            bank = Banks.query.get(args['id'])
            temp = bank
                # ==========(sentralize)=========            
            if bank == None:
                return {'status':'NOT_AVAILABLE', 'message':'Bank does not exist'}, 200, { 'Content-Type': 'application/json' }

            if bank != None:
                # Untuk bank
                if args['nama_bank'] != None:
                    bank.nama_bank = args['nama_bank']
                if args['no_rekening'] != None:
                    bank.no_rekening = args['no_rekening']
                if args['nama_pemilik'] != None:
                    bank.nama_pemilik = args['nama_pemilik']
                
                if bank.nama_bank == None:
                    bank.nama_bank = temp['nama_bank']
                if bank.no_rekening == None:
                    bank.no_rekening = temp['no_rekening']
                if bank.nama_pemilik == None:
                    bank.nama_pemilik = temp['nama_pemilik']
                db.session.commit()
                return marshal(bank, Banks.response_field), 200, { 'Content-Type': 'application/json' }
        return {'status': 'ADMIN_ONLY', 'message': 'Only for Admin'}, 404, { 'Content-Type': 'application/json' }

    @jwt_required
    def delete(self, id=None):
        if get_jwt_claims()['type'] == 'admin' or get_jwt_claims()['type'] == "superadmin":
            parser = reqparse.RequestParser()
            parser.add_argument('id', location='json', type=int)
            args = parser.parse_args()
            # return "TES"

            if id == None:
                bank = Banks.query.get(args['id'])
            if id != None:
                bank = Banks.query.get(id)

            if bank == None:
                return { 'status':'NOT_FOUND', 'message': 'Bank data not found' }, 200, { 'Content-Type': 'application/json' }
            if bank != None:
                db.session.delete(bank)
                db.session.commit()
                return { 'status':'COMPLETE', 'message': 'Delete complete' }, 200, { 'Content-Type': 'application/json' }
        return {'status': 'ADMIN_ONLY', 'message': 'Only for Admin'}, 404, { 'Content-Type': 'application/json' }


api.add_resource(BankResource,'', '/<int:id>')