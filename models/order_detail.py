from main import db

class Order_detail(db.Model):
    __tablename__ = 'order_detail'
    id_order = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float)
    order_status = db.Column(db.String(100)) 
    id_payment = db.Column(db.Integer, db.ForeignKey('payment_detail.id_payment', name='fk_oDetail_payment'))
    id_order_item = db.Column(db.Integer, db.ForeignKey('order_items.id_order_item', name='fk_oDetail_Oitem'))  
    

    payment_detail = db.relationship('Payment_detail', backref='Order_detail', foreign_keys=[id_payment])
    order_items = db.relationship('Order_items', backref='Order_detail', foreign_keys=[id_order_item]) 