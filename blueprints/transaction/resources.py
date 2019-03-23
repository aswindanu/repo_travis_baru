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
from ..stuff import *
from ..cart import *
from ..bank import *
from ..courier import *
from ..users import *

bp_transaction = Blueprint('transaction', __name__)
api = Api(bp_transaction)


#### book RESOURCE CLASS
#### All Data
class TransResource(Resource):
    @jwt_required
    def get(self, id=None):
        if id == None:
            if get_jwt_claims()['type'] == 'client' or get_jwt_claims()['type'] == 'admin':
                data_pembayaran = Transactions.query.get(get_jwt_claims()['id'])
                # return "TES"
                return marshal(data_pembayaran, Transactions.response_field), 200, { 'Content-Type': 'application/json' }
            
    @jwt_required
    def post(self):
        if get_jwt_claims()['type'] == 'client' or get_jwt_claims()['type'] == 'admin':
            parser = reqparse.RequestParser()
            parser.add_argument('pembayaran', location='json', type=int, required=True)
            parser.add_argument('pengiriman', location='json', type=int, required=True)
            args = parser.parse_args()
            
            # Fungsi memanggil tabel all
            bank = Banks.query.get(args['pembayaran'])
            courier = Couriers.query.get(args['pengiriman'])
            transaksi_detail = Transactions.query.get(get_jwt_claims()['id'])

            cart_all = Carts.query
            get_total = 0
            cart_data = []

            if cart_all == None:
                return {'status': 'NOT_FOUND', 'message': 'Anda belum membeli apapun'}, 404, { 'Content-Type': 'application/json' }

            if cart_all != None:
                for cart_marshal in cart_all:
                    cart_temp = marshal(cart_all, Carts.response_field)
                    cart_data.append(cart_temp)
            
            if len(cart_data) == 1:
                data_pembayaran = Transactions(get_jwt_claims()['id'], get_jwt_claims()['username'], cart_data['harga'], bank.nama_bank, courier.nama_kurir, "Ready to pay")
            
            if len(cart_data) > 1:
                for get_data in cart_all:
                    if get_data.username == get_jwt_claims()['username']:
                        get_total += get_data.harga
                data_pembayaran = Transactions(get_jwt_claims()['id'], get_jwt_claims()['username'], get_total, bank.nama_bank, courier.nama_kurir, "Ready to pay")
            # return "TEST"
            db.session.add(data_pembayaran)
            db.session.commit()
            return marshal(data_pembayaran, Transactions.response_field), 200, { 'Content-Type': 'application/json' }
            # # untuk cart
            # transaksi_detail.total_harga = transaksi_detail.total_harga
            # transaksi_detail.pembayaran = bank.nama_bank
            # transaksi_detail.pengiriman = courier.nama_kurir
            # transaksi_detail.status = "Ready to pay"
            # db.session.add(transaksi_detail)
            # db.session.commit()

            # return marshal(transaksi_detail, Transactions.response_field), 200, { 'Content-Type': 'application/json' }
        return {'status': 'USERS_ONLY', 'message': 'Only for users'}, 404, { 'Content-Type': 'application/json' }

    @jwt_required
    def put(self, id=None):
        if get_jwt_claims()['type'] == 'client' or get_jwt_claims()['type'] == 'admin':
            parser = reqparse.RequestParser()
            parser.add_argument('pembayaran', location='json', type=int)
            parser.add_argument('pengiriman', location='json', type=int)
            args = parser.parse_args()
            
            # ambil dari resi json
            if args['pembayaran'] != None:
                bank = Banks.query.get(args['pembayaran'])
            if args['pengiriman'] != None:
                courier = Couriers.query.get(args['pengiriman'])
            transaksi_detail = Transactions.query.get(get_jwt_claims()['id'])
            temp = transaksi_detail

            if transaksi_detail == None:
                return {'status': 'NOT_FOUND', 'message': 'Anda belum membeli apapun'}, 404, { 'Content-Type': 'application/json' }
            
            if transaksi_detail != None:
                # return "TES"
                if args['pembayaran'] != None:
                    transaksi_detail.pembayaran = bank.nama_bank
                if args['pengiriman'] != None:
                    transaksi_detail.pengiriman = courier.nama_kurir
                
                if transaksi_detail.pembayaran == None:
                    transaksi_detail.pembayaran = temp['pembayaran']
                if transaksi_detail.pengiriman == None:
                    transaksi_detail.pengiriman = temp['pengiriman']
            
            db.session.commit()
            return marshal(transaksi_detail, Transactions.response_field), 200, { 'Content-Type': 'application/json' }
        return {'status': 'USERS_ONLY', 'message': 'Only for users'}, 404, { 'Content-Type': 'application/json' }

    @jwt_required
    def delete(self, id=None):
        if get_jwt_claims()['type'] == 'client' or get_jwt_claims()['type'] == 'admin':

            transaksi_detail = Transactions.query.get(get_jwt_claims()['id'])

            db.session.delete(cart)
            db.session.commit()
            return { 'status':'COMPLETE', 'message': 'Delete complete' }, 200, { 'Content-Type': 'application/json' }
        return {'status': 'USERS_ONLY', 'message': 'Only for users'}, 404, { 'Content-Type': 'application/json' }


api.add_resource(TransResource,'', '/<int:id>')