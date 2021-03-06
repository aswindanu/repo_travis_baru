import random, logging
from blueprints import db
from flask_restful import fields
from ..stuff import *

class Carts(db.Model):
    barang = Stuffs

    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resi = db.Column(db.Integer)
    username = db.Column(db.String(50)) 
    barang = db.Column(db.String(50))
    image = db.Column(db.String(200))
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
        'image' : fields.String,
        'deskripsi' : fields.String,
        'jenis' : fields.String,
        'harga' : fields.Integer,
        'status' : fields.String,
        'jumlah' : fields.Integer
    }
    
    def __init__(self, id, resi, username, barang, image, deskripsi, jenis, harga, status, jumlah):
        self.id = id
        self.resi = resi
        self.username = username
        self.barang = barang
        self.image = image
        self.deskripsi = deskripsi
        self.jenis = jenis
        self.harga = harga
        self.status = status
        self.jumlah = jumlah

    def __repr__(self):
        return '<Cart %r>' % self.id
