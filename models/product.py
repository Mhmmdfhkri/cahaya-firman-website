from main import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Product(db.Model):
    __tablename__ = 'product'  
    id_product = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    desc = db.Column(db.String(100))
    category = db.Column(db.String(100))
    quantityInStock = db.Column(db.Integer)
    price = db.Column(db.Float)
    picture = db.Column(db.String(100))


reviews = relationship("reviews", backref="product")