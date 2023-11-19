from main import db

class Order_items(db.Model):
    __tablename__ = 'order_items'
    id_order_item = db.Column(db.Integer, primary_key=True)
    id_product = db.Column(db.Integer, db.ForeignKey('product.id_product',name='fk_order_product'))  # Foreign key ke tabel Products
    id_session = db.Column(db.Integer, db.ForeignKey('session.id_session', name='fk_order_session'))  # Foreign key ke tabel session
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    product = db.relationship('Product', backref='order_items')
    session = db.relationship('session', back_populates='order_items')
