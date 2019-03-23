import random, logging
from blueprints import db
from flask_restful import fields
from ..stuff import *
from ..cart import *

class Banks(db.Model):
    stuff = Stuffs
    cart = Carts

    __tablename__ = "bank"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_bank = db.Column(db.String(50)) 
    no_rekening = db.Column(db.Integer)
    nama_pemilik = db.Column(db.String(50))
    image = db.Column(db.String(200))

    # ===== Respon Field =====
    response_field = {
        'id': fields.Integer,
        'nama_bank' : fields.String,
        'no_rekening' : fields.Integer,
        'nama_pemilik' : fields.String,
        'image' : fields.String

    }

    def __init__(self, id, nama_bank, no_rekening, nama_pemilik, image):
        self.id = id
        self.nama_bank = nama_bank
        self.no_rekening = no_rekening
        self.nama_pemilik = nama_pemilik
        self.image = image

    def __repr__(self):
        return '<Bank %r>' % self.id