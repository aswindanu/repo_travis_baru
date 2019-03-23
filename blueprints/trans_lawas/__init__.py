import random, logging
from blueprints import db
from flask_restful import fields
from ..stuff import *

class Transactions(db.Model):
    stuff = Stuffs

    __tablename__ = "transaction"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resi = db.Column(db.Integer)
    username = db.Column(db.String(50)) 
    barang = db.Column(db.String(50))
    deskripsi = db.Column(db.String(200))
    jenis = db.Column(db.String(50))
    harga = db.Column(db.Integer)
    status = db.Column(db.String(50))
    jumlah = db.Column(db.Integer)

    # ===== Respon Field =====
    response_field = {
        'id': fields.Integer,
        'resi' : fields.Integer,
        'username' : fields.String,
        'barang' : fields.String,
        'deskripsi' : fields.String,
        'jenis' : fields.String,
        'harga' : fields.Integer,
        'status' : fields.String,
        'jumlah' : fields.Integer
    }
    
    def __init__(self, id, resi, username, barang, deskripsi, jenis, harga, status, jumlah):
        self.id = id
        self.resi = resi
        self.username = username
        self.barang = barang
        self.deskripsi = deskripsi
        self.jenis = jenis
        self.harga = harga
        self.status = status
        self.jumlah = jumlah

    def __repr__(self):
        return '<Transaction %r>' % self.id
