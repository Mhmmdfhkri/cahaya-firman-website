from main import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class cart(db.Model):
    id_cart = db.Column(db.Integer, primary_key=True)
    id_session = db.Column(db.Integer, db.ForeignKey('session.id_session'), nullable=True)
    id_product = db.Column(db.Integer, db.ForeignKey('product.id_product'), nullable=True)
    quantity = db.Column(db.Integer)


    session = relationship("session", backref="cart")  
    product = relationship("Product", backref="cart")

     

