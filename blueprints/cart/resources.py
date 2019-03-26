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
# from ..stuff import *

bp_cart = Blueprint('cart', __name__)
api = Api(bp_cart)


#### book RESOURCE CLASS
#### All Data
class CartResource(Resource):
    @jwt_required
    def get(self, id=None):
        if id == None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', location='args', type=int, default=1)
            parser.add_argument('rp', location='args', type=int, default=5)
            args = parser.parse_args()

            # Rumus (p*rp)-rp
            offset = (args['p'] * args['rp']) - args['rp']
            
            # Memunculkan data semua (ditampilkan sesuai jumlah rp)
            cart_all = Carts.query
            get_all = []

            if get_jwt_claims()['type'] == 'client':
                for get_data in cart_all:
                    if get_data.username == get_jwt_claims()['username']:
                        get_all.append(marshal(get_data, Carts.response_field))
                return get_all, 200, { 'Content-Type': 'application/json' }

            if get_jwt_claims()['type'] == 'admin' or get_jwt_claims()['type'] == "superadmin":
                for get_data in cart_all.limit(args['rp']).offset(offset).all():
                    get_all.append(marshal(get_data, Carts.response_field))
                return get_all, 200, { 'Content-Type': 'application/json' }

        else:
            if get_jwt_claims()['type'] == 'client':
                cart = Carts.query.get(id)
                if cart is not None and cart.username == get_jwt_claims()['username']:
                    return marshal(cart, Carts.response_field), 200, { 'Content-Type': 'application/json' }
                return {'status': 'NOT_FOUND', 'message': 'Anda belum membeli apapun'}, 404, { 'Content-Type': 'application/json' }

    @jwt_required
    def post(self):
        if get_jwt_claims()['type'] == 'client' or get_jwt_claims()['type'] == 'admin' or get_jwt_claims()['type'] == "superadmin":
            parser = reqparse.RequestParser()
            parser.add_argument('resi', location='json', type=int, required=True)
            parser.add_argument('jumlah', location='json', type=int, required=True)
            args = parser.parse_args()
            
            # Fungsi memanggil tabel barang
            barang = Stuffs.query.get(args['resi'])
            cart = Carts.query
            cart_data = []
            for get_data in cart:
                cart_data.append(marshal(get_data, Carts.response_field))
            # return cart_data, 200, { 'Content-Type': 'application/json' }
            
            # ==========(sentralize)==========
            calc_cart = args['jumlah']
            cart_belanja = []
            cart_other = []
            id_cart = 0
            pjg_data = len(cart_data)
            # return len(cart_data)
            # return cart[0].username
            # return cart_data[0]

            if pjg_data > 1:
                for get_data in cart:
                    # return get_data.username
                    if get_data.username == get_jwt_claims()['username']:
                        if get_data.resi == args['resi']:
                            calc_cart = get_data.jumlah + calc_cart
                            id_cart = get_data.id
                            db.session.delete(get_data)
                        if get_data.resi != args['resi']:
                            id_cart = args['resi']
                            cart_belanja.append(marshal(get_data, Carts.response_field))
                    if get_data.username != get_jwt_claims()['username']:
                        continue
            # return cart_belanja
            # return "TES"
            if pjg_data == 1 and cart[0].username == get_jwt_claims()['username'] and cart[0].resi == args['resi']:
                calc_cart = cart.jumlah + calc_cart
                id_cart = args['resi']

            if pjg_data == 0 or id_cart == 0 or id_cart == []:
                id_cart = None

                        
            # Kalkulasi sisa barang            
            calc_barang = barang.jumlah - args['jumlah']
            # return "OKE"
            if calc_barang < 0:
                return {'status':'NOT_AVAILABLE', 'message':'The quantity stuff that requested is too many'}, 200, { 'Content-Type': 'application/json' }
            if calc_barang > barang.jumlah:
                return {'status':'INVALID', 'message':"Too many stuff that you've input. Please check again"}, 200, { 'Content-Type': 'application/json' }

            barang.barang = barang.barang
            barang.image = barang.image
            barang.deskripsi = barang.deskripsi
            barang.jenis = barang.jenis
            barang.harga = barang.harga

            # jika sisa 0, maka not available
            if calc_barang == 0:
                barang.status = "Not Available"
                barang.jumlah = 0
            
            barang.status = barang.status
            barang.jumlah = calc_barang
            # return "TEST"
            db.session.commit()

            # untuk cart
            cart_add = Carts(id_cart, args['resi'], None, None, None, None, None, None, None, None)
            # return "OI"
            cart_add.username = get_jwt_claims()['username']
            cart_add.barang = barang.barang
            cart_add.image = barang.image
            cart_add.deskripsi = barang.deskripsi
            cart_add.jenis = barang.jenis
            cart_add.harga = barang.harga
            cart_add.status = "Success"
            cart_add.jumlah = calc_cart
            db.session.add(cart_add)
            db.session.commit()

            return marshal(cart_add, Carts.response_field), 200, { 'Content-Type': 'application/json' }
        return {'status': 'USERS_ONLY', 'message': 'Only for users'}, 404, { 'Content-Type': 'application/json' }

    @jwt_required
    def put(self, id=None):
        if get_jwt_claims()['type'] == 'client' or get_jwt_claims()['type'] == 'admin' or get_jwt_claims()['type'] == "superadmin":
            parser = reqparse.RequestParser()
            parser.add_argument('id', location='json', type=int, required=True)
            parser.add_argument('jumlah_tambah', location='json', type=int)
            parser.add_argument('jumlah_kurang', location='json', type=int)
            args = parser.parse_args()
            
            # ambil dari resi json
            cart = Carts.query.get(args['id'])
            # return marshal(cart, Carts.response_field), 200, { 'Content-Type': 'application/json' }
            barang = Stuffs.query.get(cart.resi)
            # return marshal(cart, Carts.response_field), 200, { 'Content-Type': 'application/json' }
            # return get_jwt_claims()['username']
            if cart.username != get_jwt_claims()['username'] or cart == None:
                return { 'status':'NOT_FOUND', 'message': 'Please check again your ID input' }, 200, { 'Content-Type': 'application/json' }

            if cart.username == get_jwt_claims()['username']:
                total_barang = barang.jumlah + cart.jumlah
                

                if args['jumlah_kurang'] != None:
                    calc_barang = barang.jumlah + args['jumlah_kurang']
                    calc_cart = cart.jumlah - args['jumlah_kurang']

                if args['jumlah_tambah'] != None:
                    calc_barang = barang.jumlah - args['jumlah_tambah']
                    calc_cart = cart.jumlah + args['jumlah_tambah']
                
                # ==========(sentralize)=========            
                if calc_barang < 0:
                    return {'status':'NOT_AVAILABLE', 'message':'This item is no longer available right now'}, 200, { 'Content-Type': 'application/json' }

                if calc_barang > total_barang:
                    return {'status':'INVALID', 'message':"Too many stuff that you've input. Please check again"}, 200, { 'Content-Type': 'application/json' }

                # Untuk barang
                barang.barang = barang.barang
                barang.image = barang.image
                barang.deskripsi = barang.deskripsi
                barang.jenis = barang.jenis
                barang.harga = barang.harga

                # jika sisa 0, maka not available
                if calc_barang == 0:
                    barang.status = "Not Available"
                    barang.jumlah = 0
                
                if  barang.status == 'Not Available' and  calc_barang > 0:
                    barang.status = 'Available'
                    barang.jumlah = calc_barang

                if barang.jumlah > 0:
                    barang.jumlah = calc_barang

                db.session.commit()

                # untuk cart
                cart.resi = cart.resi
                cart.username = cart.username
                cart.barang = cart.barang
                cart.image = cart.image
                cart.deskripsi = cart.deskripsi
                cart.jenis = cart.jenis
                cart.harga = cart.harga
                cart.status = "Success"
                cart.jumlah = calc_cart
                if cart.jumlah == 0:
                    db.session.delete(cart) 
                db.session.commit()

            return marshal(cart, Carts.response_field), 200, { 'Content-Type': 'application/json' }
        return {'status': 'USERS_ONLY', 'message': 'Only for users'}, 404, { 'Content-Type': 'application/json' }

    @jwt_required
    def delete(self, id=None):
        if get_jwt_claims()['type'] == 'client' or get_jwt_claims()['type'] == 'admin' or get_jwt_claims()['type'] == "superadmin":
            parser = reqparse.RequestParser()
            parser.add_argument('id', location='json', type=int)
            parser.add_argument('username', location='args')
            args = parser.parse_args()

            cart_all = Carts.query
            get_all = []
            temp = []

            # return cart_all[1].username
            for get_data in cart_all:
                if get_data.id == args['id'] or get_data.id == id:
                    if get_data.username == args['username'] or get_data.username == get_jwt_claims()['username']:
                        get_all.append(get_data)
                        
                # temp.append(get_data)
            
            # return marshal(get_all, Carts.response_field)
            # return get_all[0].jumlah
            if get_all == [] or get_all == None:
                return { 'status':'NOT_FOUND', 'message': 'Stuff in cart not found' }, 200, { 'Content-Type': 'application/json' }
            # return get_all, 200, { 'Content-Type': 'application/json' }
            # return "OKE"

            # if id == None:
            #     cart = Carts.query.get(args['id'])
            # if id != None:
            barang = Stuffs.query.get(get_all[0].resi)
            # return "OKE"
            #     cart = Carts.query.get(id)
            
            # if get_jwt_claims()['type'] == 'admin':
            #     if cart.username == args['username']:
            #         total_barang = barang.jumlah + cart.jumlah    

            # if get_jwt_claims()['type'] == 'client':
            #     if cart.username == get_jwt_claims()['username']:
            total_barang = barang.jumlah + get_all[0].jumlah

            barang.barang = barang.barang
            barang.image = barang.image
            barang.deskripsi = barang.deskripsi
            barang.jenis = barang.jenis
            barang.harga = barang.harga
            barang.status = barang.status
            barang.jumlah = total_barang
            db.session.commit()

            db.session.delete(get_all[0])
            db.session.commit()
            return { 'status':'COMPLETE', 'message': 'Delete complete' }, 200, { 'Content-Type': 'application/json' }
        return {'status': 'USERS_ONLY', 'message': 'Only for users'}, 404, { 'Content-Type': 'application/json' }


api.add_resource(CartResource,'', '/<int:id>')