from main import db

class Order_items(db.Model):
    __tablename__ = 'order_items'
    id_order_item = db.Column(db.Integer, primary_key=True)
    id_order = db.Column(db.Integer, db.ForeignKey('order_detail.id_order'))  # Foreign key ke tabel Orders
    id_product = db.Column(db.Integer, db.ForeignKey('product.id_product'))  # Foreign key ke tabel Products

    # Anda juga dapat menambahkan hubungan dengan objek Orders dan Products untuk mengakses data terkait.
    order = db.relationship('Order_detail', backref='Order_items')
    product = db.relationship('Product', backref='Order_items')
