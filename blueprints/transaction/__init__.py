import random, logging
from blueprints import db
from flask_restful import fields
from ..stuff import *
from ..cart import *

class Transactions(db.Model):
    stuff = Stuffs
    cart = Carts

    __tablename__ = "transaction"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50)) 
    total_harga = db.Column(db.Integer)
    pembayaran = db.Column(db.String(50))
    pengiriman = db.Column(db.String(50))
    status = db.Column(db.String(50))
    rekening_bayar = db.Column(db.Integer)
    nama_pembayar = db.Column(db.String(50))

    # ===== Respon Field =====
    response_field = {
        'id' : fields.Integer,
        'username' : fields.String,
        'total_harga' : fields.Integer,
        'pembayaran' : fields.String,
        'pengiriman' : fields.String,
        'status' : fields.String,
        'rekening_bayar' : fields.Integer,
        'nama_pembayar' : fields.String,

    }

    def __init__(self, id, username, total_harga, pembayaran, pengiriman, status, rekening_bayar, nama_pembayar):
        self.id = id
        self.username = username
        self.total_harga = total_harga
        self.pembayaran = pembayaran
        self.pengiriman = pengiriman
        self.status = status
        self.rekening_bayar = rekening_bayar
        self.nama_pembayar = nama_pembayar


    def __repr__(self):
        return '<Transaction %r>' % self.id