import random, logging
from blueprints import db
import logging, json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, abort, marshal,fields

class Users(db.Model):

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    fullname = db.Column(db.String(100))
    address = db.Column(db.String(200))
    zip_code = db.Column(db.Integer)
    image = db.Column(db.String(200))
    status = db.Column(db.String(50))

    # ===== Respon Field =====
    response_field = {
        'id' : fields.Integer,
        'type' : fields.String,
        'username' : fields.String,
        'password' : fields.String,
        'fullname' : fields.String,
        'address' : fields.String,
        'zip_code' : fields.Integer,
        'image' : fields.String,
        'status' : fields.String
    }
    
    def __init__(self, id, type, username, password, fullname, address, zip_code, image, status):
        self.id = id
        self.type = type
        self.username = username
        self.password = password
        self.fullname = fullname
        self.address = address
        self.zip_code = zip_code
        self.image = image
        self.status = status

    def __repr__(self):
        return '<User %r>' % self.id