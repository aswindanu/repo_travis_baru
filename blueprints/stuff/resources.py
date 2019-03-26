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

bp_barang = Blueprint('barang', __name__)
api = Api(bp_barang)


#### book RESOURCE CLASS
#### All Data
class BarangResource(Resource):
    def get(self, id=None):
        if id == None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', location='args', type=int, default=1)
            parser.add_argument('rp', location='args', type=int, default=12)
            parser.add_argument('barang', location='args')
            parser.add_argument('jenis', location='args')
            parser.add_argument('resi', location='args')
            args = parser.parse_args()

            # Rumus (p*rp)-rp
            offset = (args['p'] * args['rp']) - args['rp']
            
            # Memunculkan data semua (ditampilkan sesuai jumlah rp)
            # return args['resi']
            if args['resi'] is not None:
                barang_all = Stuffs.query.get(args['resi'])
                return marshal(barang_all, Stuffs.response_field), 200, { 'Content-Type': 'application/json' }
            
            barang_all = Stuffs.query

            # search dari nama barang
            if args['barang'] is not None:
                barang_all = barang_all.filter(Stuffs.barang.like("%"+args['barang']+"%"))
            
            # search dari jenis barang
            if args['jenis'] is not None:
                barang_all = barang_all.filter(Stuffs.jenis.like("%"+args['jenis']+"%"))

            get_all = []
            for get_data in barang_all.all():
                get_all.append(marshal(get_data, Stuffs.response_field))
            return get_all, 200, { 'Content-Type': 'application/json' }
            
        else:
            barang = Stuffs.query.get(id)
            if barang is not None:
                return marshal(barang, Stuffs.response_field), 200, { 'Content-Type': 'application/json' }
            return {'status': 'NOT_FOUND', 'message': 'Book not found'}, 404, { 'Content-Type': 'application/json' }

    @jwt_required
    def post(self):
        if get_jwt_claims()['type'] == 'admin' or get_jwt_claims()['type'] == "superadmin":
            parser = reqparse.RequestParser()
            resi = random.randrange(10000000, 99999999)
            parser.add_argument('barang', location='json', required=True)
            parser.add_argument('image', location='json', required=True)
            parser.add_argument('deskripsi', location='json', required=True)
            parser.add_argument('jenis', location='json', required=True)
            parser.add_argument('harga', location='json',  type=int, required=True)
            parser.add_argument('jumlah', location='json', type=int, required=True)
            args = parser.parse_args()
            
            # ==========(sentralize)==========
            barang = Stuffs(resi, args['barang'], args['image'], args['deskripsi'], args['jenis'], args['harga'], 'Available', args['jumlah'])
            db.session.add(barang)
            db.session.commit()
            return marshal(barang, Stuffs.response_field), 200, { 'Content-Type': 'application/json' }
        return { 'status': 'ADMIN_ONLY', 'message': 'Only allowed for admin' }, 404, { 'Content-Type': 'application/json' }

    @jwt_required
    def put(self, id=None):
        if get_jwt_claims()['type'] == 'admin' or get_jwt_claims()['type'] == "superadmin":
            parser = reqparse.RequestParser()
            parser.add_argument('resi', location='json')
            parser.add_argument('barang', location='json')
            parser.add_argument('image', location='json')
            parser.add_argument('deskripsi', location='json')
            parser.add_argument('jenis', location='json')
            parser.add_argument('harga', location='json',  type=int)
            parser.add_argument('status', location='json')
            parser.add_argument('jumlah', location='json')
            args = parser.parse_args()

            # ambil dari resi json
            if id == None:
                barang = Stuffs.query.get(args['resi'])
            
            # ambil dari resi (ditulis website)
            if id != None:
                barang = Stuffs.query.get(id) 
            
            temp = barang
            # return temp.status
                # ==========(sentralize)=========
            if barang != None:
                if args['barang'] != None or args['barang'] != "":
                    barang.barang = args['barang']
                if args['image'] != None or args['image'] != "":
                    barang.image = args['image']
                if args['deskripsi'] != None or args['deskripsi'] != "":
                    barang.deskripsi = args['deskripsi']
                if args['jenis'] != None or args['jenis'] != "":
                    barang.jenis = args['jenis']
                if args['harga'] != None or args['harga'] != "":
                    barang.harga = args['harga']
                if temp.jumlah == "0":
                    barang.status = temp.status
                if temp.jumlah != "0":
                    barang.status = 'Available'
                if args['status'] != None or args['status'] != "":
                    barang.status = args['status']
                if args['jumlah'] != None or args['jumlah'] != "":
                    barang.jumlah = args['jumlah']
                db.session.commit()
                return marshal(barang, Stuffs.response_field), 200, { 'Content-Type': 'application/json' }
                
                if barang.barang == None or barang.barang == "":
                    barang.barang = temp.barang
                if barang.image == None or barang.image == "":
                    barang.image = temp.image
                if barang.deskripsi == None or barang.deskripsi == "":
                    barang.deskripsi = temp.image
                if barang.jenis == None or barang.jenis == "":
                    barang.jenis = temp.jenis
                if barang.harga == None or barang.harga == "":
                    barang.harga = temp.harga
                if barang.status == None or barang.status == "":
                    if temp.jumlah == "0":
                        barang.status = temp.status
                    if temp.jumlah != "0":
                        barang.status = 'Available'
                if barang.jumlah == None or barang.jumlah == "":
                    barang.jumlah = temp.jumlah

            if barang == None:
                return { 'status': 'NOT_FOUND', 'message': 'Stuff not found' }, 404, { 'Content-Type': 'application/json' }                
        return { 'status': 'ADMIN_ONLY', 'message': 'Only allowed for admin' }, 404, { 'Content-Type': 'application/json' }

    @jwt_required
    def delete(self, id=None):
        if get_jwt_claims()['type'] == 'admin' or get_jwt_claims()['type'] == "superadmin":
            parser = reqparse.RequestParser()
            parser.add_argument('resi', location='json', type=int)
            args = parser.parse_args()
        
            if id != None:
                barang = Stuffs.query.get(id)

            if id == None:
                barang = Stuffs.query.get(args['resi'])

            if barang != None:
                db.session.delete(barang)
                db.session.commit()
                return { 'status':'COMPLETE', 'message': 'Delete complete' }, 200, { 'Content-Type': 'application/json' }
            return { 'status': 'NOT_FOUND', 'message': 'Stuff not found' }, 404, { 'Content-Type': 'application/json' }
        return { 'status': 'ADMIN_ONLY', 'message': 'Only allowed for admin' }, 404, { 'Content-Type': 'application/json' }

api.add_resource(BarangResource,'', '/<int:id>')