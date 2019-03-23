import random, logging
from blueprints import db
from flask_restful import fields
from ..stuff import *
from ..cart import *

class Couriers(db.Model):
    stuff = Stuffs
    cart = Carts

    __tablename__ = "courier"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_kurir = db.Column(db.String(50)) 
    mode_pengiriman = db.Column(db.String(50))

    # ===== Respon Field =====
    response_field = {
        'id': fields.Integer,
        'nama_kurir' : fields.String,
        'mode_pengiriman' : fields.String
    }
    
    def __init__(self, id, nama_kurir, mode_pengiriman):
        self.id = id
        self.nama_kurir = nama_kurir
        self.mode_pengiriman = mode_pengiriman

    def __repr__(self):
        return '<Courier %r>' % self.id