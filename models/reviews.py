from main import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class reviews(db.Model):
    id_reviews = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=True)
    id_product = db.Column(db.Integer, db.ForeignKey('product.id_product'), nullable=True)
    comment = db.Column(db.String(250), nullable=True, unique=False)
    rating = db.Column(db.Integer, nullable=True, unique=False)

    user = relationship("User", backref="reviews")  
    product = relationship("Product", backref="reviews")

    