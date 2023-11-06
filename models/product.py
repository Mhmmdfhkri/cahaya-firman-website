from main import db

class Product(db.Model):
    __tablename__ = 'product'  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    desc = db.Column(db.String(100))
    category = db.Column(db.String(100))
    quantityInStock = db.Column(db.Integer)
    price = db.Column(db.Float)
    picture = db.Column(db.String(100))
