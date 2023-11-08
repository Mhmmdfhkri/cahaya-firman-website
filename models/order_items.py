from main import db

class Order_items(db.Model):
    __tablename__ = 'order_items'
    id_order_item = db.Column(db.Integer, primary_key=True)
    id_order = db.Column(db.Integer, db.ForeignKey('orders.id_order'))  # Foreign key ke tabel Orders
    id_product = db.Column(db.Integer, db.ForeignKey('products.id_product'))  # Foreign key ke tabel Products

    # Anda juga dapat menambahkan hubungan dengan objek Orders dan Products untuk mengakses data terkait.
    order = db.relationship('order_detail', backref='order_items')
    product = db.relationship('product', backref='order_items')
