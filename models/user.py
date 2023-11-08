from flask_login import UserMixin
from main import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class User(db.Model, UserMixin):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False) 
    fullname = db.Column(db.String(60), nullable=True, unique=False)
    gender = db.Column(db.CHAR(1), nullable=True, unique=False)
    telephone = db.Column(db.Integer, nullable=True, unique=False)
    address = db.Column(db.String(60), nullable=True, unique=False)
    def get_id(self):
           return (self.id_user)

    